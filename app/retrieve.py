import math

from pydantic import BaseModel

class RetrievalFilters(BaseModel):
    source: str | None = None
    document_type: str | None = None

def cosine_similarity(left: list[float], right: list[float]) -> float:
    """
    left: list[float], the left vector
            [0.1, 0.2, 0.3, ...]
    right: list[float], the right vector
    
    return: float, the cosine similarity between left and right
    """
    if len(left) != len(right):
        raise ValueError("Vectors must have the same length")
    if not right:
        raise ValueError("Vectors must not be empty")

    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))

    if left_norm == 0 or right_norm == 0:
        return 0.0

    return round(dot / (left_norm * right_norm), 6)


def rank_chunks_by_similarity(
    query_embedding: list[float],
    chunks: list[dict],
    top_k: int = 3,
) -> list[dict]:
    """
    query_embedding: list[float], the query vector
    chunks: list[dict], a list of chunks, each chunk is a dict with chunk_id and embedding
                [
                    {
                        "chunk_id": "123",
                        "embedding": [0.1, 0.2, 0.3],
                        ...
                    },
                ]
    top_k: int, return the top_k chunks with highest similarity
    
    return: list[dict], a list of chunks, each chunk is a dict with chunk_id and score
                [
                    {
                        "chunk_id": "123",
                        "score": 0.8,
                        ...
                    },
                ]
    """
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    scored = []
    for chunk in chunks:
        embedding = chunk.get("embedding")
        if embedding is None:
            continue

        row = dict(chunk)
        row["score"] = cosine_similarity(query_embedding, embedding)
        scored.append(row)

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


def normalize_retrieval_filters(
        filters: RetrievalFilters | None
) -> dict | None:
    """Convert optional API filter fields into a clean dict for vector search."""
    if filters is None:
        return None

    normalized = {}
    for key, value in filters.model_dump(exclude_none=True).items():
        if isinstance(value, str):
            value = value.strip()
            # Swagger users may type Python-like None; treat it as no filter.
            if value.lower() in {"", "none", "null"}:
                continue
        normalized[key] = value

    return normalized or None