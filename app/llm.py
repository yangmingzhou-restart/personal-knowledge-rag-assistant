from abc import ABC, abstractmethod
import httpx
from app.config import settings

#RAG核心不只是“把资料塞给LLM”，而是让LLM知道：哪些是资料，哪些是问题，不能做什么，答案要如何引用来源。
# question + retrieved chunks -> build_grounded_prompt(...)
# -> strict context block -> LLM answer grounded in sources

class LLMProviderError(Exception):
    """Raised when an LLM provider cannot generate a response safely."""

class LLMClient(ABC):
    """
    LLMClient abstract boundary.

    Function:
        Unify the interface of different LLM providers, so that 
        we can switch switch between providers.
    
    Main methods:
        generate(prompt): generate answer from prompt by LLM
        
    RAG process position:
        in /answer, generating the answer with question and uploaded documents by LLM.
    """
    @abstractmethod
    def generate(self, prompt: str) -> dict[str, str]:
        """
        prompt: str, the prompt to answer the question
        return: dict[str, str], the answer from LLM provider
            {
                "answer": "LLM_generated_answer",
                "provider": LLMClient,
            }
        """
        raise NotImplementedError
    
class FakeLLMClient(LLMClient):
    def generate(self, prompt: str) -> dict[str, str]:
        preview = prompt.replace("\n", " ")[:450]
        return {
            "answer": f"FAKE_ANSWER: {preview}",
            "provider": "fake",
        }

class FakeFailingLLMClient(LLMClient):
    def generate(self, prompt: str) -> dict[str, str]:
        raise LLMProviderError("Fake LLM provider failed")

class OllamaLLMClient(LLMClient):
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11434",
        model: str = "qwen2.5:3b",
        timeout_seconds: float = 60.0,
    ) -> None:
        self.base_url = base_url
        self.model = model
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str) -> dict[str, str]:
        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    # 关闭流式输出，方便API层一次性拿到完整 answer
                    "stream": False,
                },
                timeout=self.timeout_seconds,
            )
            response.raise_for_status() #错误状态码直接抛出异常
        except httpx.HTTPError as exc:
            raise LLMProviderError("Ollama provider failed") from exc
        
        payload = response.json()
        answer = payload.get("response")
        if not isinstance(answer, str) or not answer.strip():
            raise LLMProviderError("Ollama provider returned an empty answer")
        
        return {
            "answer": answer,
            "provider": f"ollama:{self.model}",
        }

_llm_cache_flag : bool = False
def get_llm_client() -> LLMClient:
    """
    Get LLMClient instance based on the provider in settings of config.py.
    """
    global _llm_cache_flag
    provider = settings.llm_provider.lower()

    _llm_cache_flag = True # llm model loaded

    if provider == "fake":
        return FakeLLMClient()

    if provider == "failing_fake":
        return FakeFailingLLMClient()
    
    if provider == "ollama":
        return OllamaLLMClient(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )
    
    _llm_cache_flag = False # llm model not loaded
    raise LLMProviderError(f"Unsupported LLM provider: {provider}")

def load_ollama_model() ->dict[str, str]:
    """
    Manually load Ollama model

    Function:
        Post a prompt, then ollama load the model.
        Load the Ollama model instance in Swagger by clicking the button.
    """
    response = httpx.post(
        f"{settings.ollama_base_url}/api/generate",
        json={
            "model": settings.ollama_model,
            "prompt": "ping",
            "stream": False,
            "keep_alive": "10m",
        },
        timeout=120,
    )
    response.raise_for_status()

    return {
        "status": "loaded",
        "model": settings.ollama_model,
    }

def unload_ollama_model() -> None:
    """
    Manually unload Ollama model

    Function:
        Post keep_alive=0, then ollama release the model.
        Unload the Ollama model instance in Swagger by clicking the button.
    """
    global _llm_cache_flag

    response = httpx.post(
        f"{settings.ollama_base_url}/api/generate",
        json={
            "model": settings.ollama_model,
            "prompt": "",
            "stream": False,
            "keep_alive": 0,
        },
        timeout=120,
    )
    response.raise_for_status()
    
    _llm_cache_flag = False # llm model unload

    return {
        "status": "unloaded",
        "model": settings.ollama_model,
    }
