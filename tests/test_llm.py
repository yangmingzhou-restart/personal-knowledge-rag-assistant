from app.llm import FakeLLMClient, get_llm_client, FakeFailingLLMClient, LLMProviderError
import pytest

def test_fake_llm_client_returns_deterministic_answer():
    client = FakeLLMClient()

    result = client.generate(
        prompt="Question: What does RAG use?\nContext: RAG uses retrieved context."
    )
    
    assert result["answer"].startswith("FAKE_ANSWER:")
    assert "RAG uses retrieved context" in result["answer"]
    assert result["provider"] == "fake"

def test_get_llm_client_default_to_fake():
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
    monkeypatch.setenv("LLM_PROVIDER", "unknown")

    with pytest.raises(LLMProviderError):
        get_llm_client()
