import os
from abc import ABC, abstractmethod

#RAG核心不只是“把资料塞给LLM”，而是让LLM知道：哪些是资料，哪些是问题，不能做什么，答案要如何引用来源。
# question + retrieved chunks -> build_grounded_prompt(...)
# -> strict context block -> LLM answer grounded in sources

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
    
def get_llm_client() -> LLMClient:
    provider = os.getenv("LLM_PROVIDER", "fake").lower()
    
    if provider == "fake":
        return FakeLLMClient()
    
    raise ValueError(f"Unsupported LLM provider: {provider}")
