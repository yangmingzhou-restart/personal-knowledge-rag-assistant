from abc import ABC, abstractmethod
import httpx
from app.config import settings

#RAG核心不只是“把资料塞给LLM”，而是让LLM知道：哪些是资料，哪些是问题，不能做什么，答案要如何引用来源。
# question + retrieved chunks -> build_grounded_prompt(...)
# -> strict context block -> LLM answer grounded in sources

class LLMProviderError(Exception):
    """Raised when an LLM provider cannot generate a response safely."""

class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> dict[str, str]:
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


def get_llm_client() -> LLMClient:
    provider = settings.llm_provider.lower()
    
    if provider == "fake":
        return FakeLLMClient()

    if provider == "failing_fake":
        return FakeFailingLLMClient()
    
    if provider == "ollama":
        return OllamaLLMClient(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )
    
    raise LLMProviderError(f"Unsupported LLM provider: {provider}")


