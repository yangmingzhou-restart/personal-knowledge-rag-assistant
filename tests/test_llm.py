from app.llm import FakeLLMClient, get_llm_client

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
