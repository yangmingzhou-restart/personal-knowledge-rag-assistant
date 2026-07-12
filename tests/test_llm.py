import pytest
import httpx
from app.config import settings


from app.llm import (
                    FakeLLMClient, 
                    get_llm_client, 
                    FakeFailingLLMClient, 
                    LLMProviderError,
                    OllamaLLMClient,
                    )

def test_fake_llm_client_returns_deterministic_answer():
    client = FakeLLMClient()

    result = client.generate(
        prompt="Question: What does RAG use?\nContext: RAG uses retrieved context."
    )
    
    assert result["answer"].startswith("FAKE_ANSWER:")
    assert "RAG uses retrieved context" in result["answer"]
    assert result["provider"] == "fake"

def test_get_llm_client_default_to_fake(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", "fake")

    client = get_llm_client()

    result = client.generate("hello")

    assert result["provider"] == "fake"

def test_fake_llm_client_returns_answer_and_provider():
    client = FakeLLMClient()

    result = client.generate("hello")

    assert result["provider"] == "fake"
    assert "FAKE_ANSWER" in result["answer"]

def test_fake_failing_llm_client_raises_provider_error():
    client = FakeFailingLLMClient()

    with pytest.raises(LLMProviderError):
        client.generate("hello")
    
def test_get_llm_client_rejects_unsupported_provider(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", "unknown")

    with pytest.raises(LLMProviderError):
        get_llm_client()

def test_get_llm_client_selects_ollama(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", "ollama")
    monkeypatch.setattr(settings, "ollama_base_url", "http://127.0.0.1:11434")
    monkeypatch.setattr(settings, "ollama_model", "qwen2.5:3b")

    client = get_llm_client()

    assert isinstance(client, OllamaLLMClient)
    assert client.model == settings.ollama_model

def test_ollama_llm_client_generate_answer(monkeypatch):
    def fake_post(url, json, timeout):
        assert url == "http://127.0.0.1:11434/api/generate"
        assert json["model"] == "qwen2.5:3b"
        assert json["stream"] is False

        request = httpx.Request("POST", url)
        return httpx.Response(200, 
                              json={"response": "grounded answer"},
                              request=request)
    
    monkeypatch.setattr(httpx, "post", fake_post)

    client = OllamaLLMClient(
        base_url="http://127.0.0.1:11434",
        model="qwen2.5:3b",
    )

    result = client.generate("Question: what is RAG?")

    assert result == {
        "answer": "grounded answer",
        "provider": "ollama:qwen2.5:3b",
    }

def test_ollama_llm_client_raises_privder_error_on_request_failure(monkeypatch):
    def fake_post(url, json, timeout):
        raise httpx.ConnectError("connection failed")
    
    monkeypatch.setattr(httpx, "post", fake_post)
    client = OllamaLLMClient()

    with pytest.raises(LLMProviderError):
        client.generate("hello")
