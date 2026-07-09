import math


def cosine_similarity(left: list[float], right: list[float]) -> float:
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
