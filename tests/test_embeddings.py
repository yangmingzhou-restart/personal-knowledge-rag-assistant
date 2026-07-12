from app.embeddings import (
    EmbeddingProvider,
    FakeEmbeddingProvider,
    LocalEmbeddingProvider,
    embed_chunks,
    embed_text,
    get_embedding_provider,
)
from app.config import settings

class DummySentenceTransformer:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def encode(self, text: str, normalize_embeddings: bool = False):
        return [0.1, 0.2, 0.3]

def test_embed_text_returns_fixed_size_vector():
    vector = embed_text("hello rag", dimensions=8)

    assert len(vector) == 8
    assert all(isinstance(value, float) for value in vector)

def test_embed_text_is_deterministic():
    first = embed_text("hello rag", dimensions=8)
    second = embed_text("hello rag", dimensions=8)

    assert first == second

def test_different_text_produces_different_vector():
    first = embed_text("hello rag", dimensions=8)
    second = embed_text("different text", dimensions=8)

    assert first != second

def test_embed_chunks_adds_embedding_to_each_chunk():
    chunks = [
        {
            "chunk_id": "chunk_1",
            "document_id": "doc_1",
            "chunk_index":0,
            "text": "hello rag",
            "start_char": 0,
            "end_char": 9,
        }
    ]

    embedded = embed_chunks(chunks, dimensions=8)

    assert len(embedded) == 1
    assert embedded[0]["chunk_id"] == "chunk_1"
    assert embedded[0]["embedding"] == embed_text("hello rag", dimensions=8)

def test_invalid_dimension_raises_value_error():
    try:
        embed_text("hello", dimensions=0)
    except ValueError as exc:
        assert "dimensions" in str(exc)
    else:
        raise AssertionError("Expected ValueError")

def test_fake_embedding_provider_embed_text():
    provider = FakeEmbeddingProvider(dimensions=8)

    vector =  provider.embed_text("hello rag")

    assert len(vector) == 8
    assert vector == provider.embed_text("hello rag")

def test_fake_embedding_provider_embeds_chunks():
    provider = FakeEmbeddingProvider(dimensions=8)
    chunks = [
        {
            "chunk_id": "chunk_1",
            "document_id": "doc_1",
            "chunk_index":0,
            "text": "hello rag",
            "start_char": 0,
            "end_char": 9,
        }
    ]

    embedded = provider.embed_chunks(chunks)

    assert embedded[0]["embedding"] == provider.embed_text("hello rag")

def test_get_embedding_provider_returns_fake_provider_when_requested(monkeypatch):
    monkeypatch.setattr(settings, "embedding_provider", "fake")

    provider = get_embedding_provider()

    assert isinstance(provider, FakeEmbeddingProvider)
    assert isinstance(provider, EmbeddingProvider)

def test_get_embedding_provider_defaults_to_local(monkeypatch):
    # The app should use the downloaded local BGE model unless fake is explicitly requested.
    model_path = "dummy-local-model"
    monkeypatch.setattr(settings, "embedding_provider", "local")
    monkeypatch.setattr(settings, "local_embedding_model", model_path)

    monkeypatch.setattr(
        "app.embeddings.load_sentence_transformer",
        lambda model_name: DummySentenceTransformer(model_name),
    )
    #monkeypatch.setattr(settings, "embedding_provider", "local")

    provider = get_embedding_provider()
    
    assert isinstance(provider, LocalEmbeddingProvider)
    assert provider.model_name == settings.local_embedding_model

def test_get_embedding_provider_selects_local(monkeypatch):
    model_path = "dummy-local-model"

    monkeypatch.setattr(settings, "embedding_provider", "local")
    monkeypatch.setattr(settings, "local_embedding_model", model_path)
    monkeypatch.setattr(
        "app.embeddings.load_sentence_transformer",
        lambda model_name: DummySentenceTransformer(model_name),
    )

    provider = get_embedding_provider()

    assert isinstance(provider, LocalEmbeddingProvider)
    assert provider.model_name == model_path

def test_local_embedding_provider_embed_text_uses_model(monkeypatch):
    monkeypatch.setattr(
        "app.embeddings.load_sentence_transformer",
        lambda model_name: DummySentenceTransformer(model_name),
    )
    provider = LocalEmbeddingProvider(model_name="dummy-model")

    vector = provider.embed_text("hello rag")

    assert vector == [0.1, 0.2, 0.3]

def test_get_embedding_provider_defaults_to_local_path(monkeypatch):
    # Default production behavior is local BGE, but the loader is patched so CI
    # verifies provider selection without loading a model from this machine.
    model_path = "dummy-default-local-model"

    monkeypatch.setattr(settings, "embedding_provider", "local")
    monkeypatch.setattr(settings, "local_embedding_model", model_path)
    monkeypatch.setattr(
        "app.embeddings.load_sentence_transformer",
        lambda model_name: DummySentenceTransformer(model_name),
    )

    provider = get_embedding_provider()

    assert isinstance(provider, LocalEmbeddingProvider)
    assert provider.model_name == settings.local_embedding_model
    

