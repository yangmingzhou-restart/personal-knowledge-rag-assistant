from app.embeddings import (
    DEFAULT_LOCAL_EMBEDDING_MODEL,
    EmbeddingProvider,
    FakeEmbeddingProvider,
    LocalEmbeddingProvider,
    embed_chunks,
    embed_text,
    get_embedding_provider,
)


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
    monkeypatch.setenv("EMBEDDING_PROVIDER", "fake")

    provider = get_embedding_provider()

    assert isinstance(provider, FakeEmbeddingProvider)
    assert isinstance(provider, EmbeddingProvider)

def test_get_embedding_provider_defaults_to_local(monkeypatch):
    # The app should use the downloaded local BGE model unless fake is explicitly requested.
    monkeypatch.delenv("EMBEDDING_PROVIDER", raising=False)
    monkeypatch.setattr(
        "app.embeddings.load_sentence_transformer",
        lambda model_name: DummySentenceTransformer(model_name),
    )

    provider = get_embedding_provider()
    
    assert isinstance(provider, LocalEmbeddingProvider)
    assert provider.model_name == DEFAULT_LOCAL_EMBEDDING_MODEL

def test_get_embedding_provider_selects_local(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "local")
    monkeypatch.setenv("LOCAL_EMBEDDING_MODEL", r"D:\AI创业\AI模型\embedding-models\BAAI\bge-small-zh-v1.5")
    monkeypatch.setattr(
        "app.embeddings.load_sentence_transformer",
        lambda model_name: DummySentenceTransformer(model_name),
    )

    provider = get_embedding_provider()

    assert isinstance(provider, LocalEmbeddingProvider)
    assert provider.model_name == r"D:\AI创业\AI模型\embedding-models\BAAI\bge-small-zh-v1.5"

def test_local_embedding_provider_embed_text_uses_model(monkeypatch):
    monkeypatch.setattr(
        "app.embeddings.load_sentence_transformer",
        lambda model_name: DummySentenceTransformer(model_name),
    )
    provider = LocalEmbeddingProvider(model_name="dummy-model")

    vector = provider.embed_text("hello rag")

    assert vector == [0.1, 0.2, 0.3]

