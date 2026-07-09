import hashlib
from abc import ABC, abstractmethod


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
    return FakeEmbeddingProvider()


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
