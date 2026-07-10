import hashlib
from abc import ABC, abstractmethod
import os

DEFAULT_LOCAL_EMBEDDING_MODEL = r"D:\AI创业\AI模型\embedding-models\BAAI\bge-small-zh-v1.5"


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError

    @abstractmethod
    def embed_chunks(
        self,
        chunks: list[dict[str, str | int]],
    ) -> list[dict[str, str | int | list[float]]]:
        raise NotImplementedError

def load_sentence_transformer(model_name: str):
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str = DEFAULT_LOCAL_EMBEDDING_MODEL) -> None:
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

def get_embedding_provider() -> EmbeddingProvider:
    # Default is local BGE; set EMBEDDING_PROVIDER=fake only for tests/CI.
    provider = os.getenv("EMBEDDING_PROVIDER", "local").lower()
    
    if provider == "fake":
        return FakeEmbeddingProvider()
    elif provider == "local":
        model_name = os.getenv(
            "LOCAL_EMBEDDING_MODEL",
            DEFAULT_LOCAL_EMBEDDING_MODEL,
        )
        return LocalEmbeddingProvider(model_name=model_name)
     
    raise ValueError("Unsupported embedding provider")
    

def embed_text(text: str, dimensions: int = 16) -> list[float]:
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
    embedded = []
    for chunk in chunks:
        row = dict(chunk)
        row["embedding"] = embed_text(str(chunk["text"]), dimensions=dimensions)
        embedded.append(row)

    return embedded
