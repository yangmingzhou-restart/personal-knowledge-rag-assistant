import hashlib
from abc import ABC, abstractmethod
from app.config import settings

class EmbeddingProvider(ABC):
    """
    Embedding provider abstract boundary.

    Functions:
        Unify the calling method of "text -> vector", so that processes such as 
        upload, retrieve, and answer do not need to be concerned about whether 
        to use which embeddings (fake, local, future API...)
    
    Main methods:
        embed_text(text): Convert text to embedding vector, list[float]
        embed_chunks(chunks): Add the embedding to each chunk in chunks list, list[dict[str, str | int | list[float]]]
    
    RAG process position:
        After chunking, before vector_store and similarity search.
    """
    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """
        text: str, the text to be embedded, usually a single chunk text
        return: list[float], the embedding vector of the text
                it will be used to calculate the cosine similarity in retrieve process.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_chunks(
        self,
        chunks: list[dict[str, str | int]],
    ) -> list[dict[str, str | int | list[float]]]:
        """
        chunks: list[dict[str, str | int]], the chunks to be embedded
        return: list[dict[str, str | int | list[float]]], the chunks with embedding field added
                [
                    {
                        "chunk_id": "chunk_1",
                        "document_id": "doc_1",
                        "chunk_index": 0,
                        "text": "Hello, world!",
                        "start_char": 0,
                        "end_char": 11,
                        "created_at": "2023-01-01T00:00:00+00:00",
                        "embedding": [0.34, 0.98],
                    },
                    {
                    ...
                    },
                    ...
                ]
        """ 
        raise NotImplementedError

def load_sentence_transformer(model_name: str):
    """
    model_name: str, the name of the sentence transformer model
    return: SentenceTransformer, the loaded sentence transformer model
            returned model can be used to embed text to vector.
    """
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str = settings.local_embedding_model) -> None:
        # Keep model_name configurable so we can later switch to BAAI/bge-m3.
        self.model_name = model_name
        self.model = load_sentence_transformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        # Normalized vectors make cosine similarity more stable.
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
    
    def embed_chunks(
            self,
            chunks: list[dict[str, str | int]],
        ) -> list[dict[str, str | int | list[float]]]:
        embedded = []
        for chunk in chunks:
            row = dict(chunk)
            # Keep the output shape identical to FakeEmbeddingProvider
            row["embedding"] = self.embed_text(str(chunk["text"]))
            embedded.append(row)
        return embedded
        
class FakeEmbeddingProvider(EmbeddingProvider):
    def __init__(self, dimensions: int = 16) -> None:
        self.dimensions = dimensions

    def embed_text(self, text: str) -> list[float]:
        return embed_text(text, dimensions=self.dimensions)

    def embed_chunks(
        self,
        chunks: list[dict[str, str | int]],
    ) -> list[dict[str, str | int | list[float]]]:
        return embed_chunks(chunks, dimensions=self.dimensions)

_embedding_provider_cache: EmbeddingProvider | None = None # Cache the embedding provider instance
def get_embedding_provider() -> EmbeddingProvider:
    """
    return: EmbeddingProvider, the embedding provider instance
            the model depends on the settings.embedding_provider
    """
    # Default is local BGE; set EMBEDDING_PROVIDER=fake only for tests/CI.
    global _embedding_provider_cache

    if _embedding_provider_cache is not None:
        return _embedding_provider_cache
    
    provider = settings.embedding_provider.lower()
    
    if provider == "fake":
        _embedding_provider_cache = FakeEmbeddingProvider()
        return _embedding_provider_cache
    
    if provider == "local":
        _embedding_provider_cache = LocalEmbeddingProvider(
            model_name=settings.local_embedding_model
        )
        return _embedding_provider_cache
        
    raise ValueError(f"Unsupported embedding provider: {provider}")


def embed_text(text: str, dimensions: int = 16) -> list[float]:
    """
    text: str, the text to be embedded, usually a single chunk text
    dimensions: int, the dimension of the embedding vector
    return: list[float], the embedding vector of the text
            it will be used to calculate the cosine similarity in retrieve process.
    """
    if dimensions <= 0:
        raise ValueError("dimensions must be greater than 0")

    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = []

    while len(values) < dimensions:
        for byte in digest:
            values.append(round(byte / 256, 6))
            if len(values) == dimensions:
                break
        digest = hashlib.sha256(digest).digest()

    return values


def embed_chunks(
    chunks: list[dict[str, str | int]],
    dimensions: int = 16,
) -> list[dict[str, str | int | list[float]]]:
    """
    chunks: list[dict[str, str | int]], the chunks to be embedded
    dimensions: int, the dimension of the embedding vector
    return: list[dict[str, str | int | list[float]]], the chunks with embedding field added
    """
    embedded = []
    for chunk in chunks:
        row = dict(chunk)
        row["embedding"] = embed_text(str(chunk["text"]), dimensions=dimensions)
        embedded.append(row)

    return embedded

def reset_embedding_provider_cache() -> None:
    """
    Clear the embedding provider cache

    when monkeypatch setattr(), the cache should be cleared.
    """
    global _embedding_provider_cache
    _embedding_provider_cache = None
