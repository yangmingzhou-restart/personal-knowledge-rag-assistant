from abc import  ABC, abstractmethod
from app.config import settings

class Reranker(ABC):
    """
    Function:
        Reorder retrieved candidate chunks after vector search.

    Main methods:
    rerank(question, matches, top_k): return final top_k chunks.

    RAG process position:
        After vector retrieval, before prompt construction or API response.
    """

    @abstractmethod
    def rerank(
        self, 
        question:str, 
        matches:list[dict],
        top_k: int
    ) -> list[dict]:
        """
        Reorder retrieved candidate chunks after vector search.
        Choose top_k embeddings from matches (whose length >= top_k).
        [
            {
                "chunk_id": "123",
                "score": 0.5,
                "rerank_score": 0.8,
                "candidate_rank": 1,
            }
        ]
        """
        raise NotImplementedError

class KeywordOverlapReranker(Reranker):
    """Deterministic reranker for tests and CI; not a real semantic reranker."""

    def rerank(
            self,
            question: str,
            matches: list[dict],
            top_k: int,
    ) -> list[dict]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        query_terms = set(question.lower().split())
        scored = []

        for index, match in enumerate(matches):
            text_terms = set(str(match.get("text", "")).lower().split())
            rerank_score = len(query_terms & text_terms)
            row = dict(match)
            row["rerank_score"] = rerank_score
            row["candidate_rank"] = index + 1
            scored.append(row)

        # Tie-break with original vector score so we preserve vector retrieval signal.
        scored.sort(
            key=lambda item: (item["rerank_score"], item.get("score", 0)),
            reverse=True,
        )
        return scored[:top_k]
    
_reranker_provider_cache: Reranker | None = None
class CrossEncoderReranker(Reranker):
    """Real reranker backed by a cross-encoder model; use only for local demos."""

    def __init__(self, model_name: str):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(model_name)

    def rerank(self, question: str, matches: list[dict], top_k: int) -> list[dict]:
        if top_k <= 0:
            raise ValueError("top_k must greater than 0")
        
        # 创建 (question, document) 对, list[tuple]
        pairs = [(question, str(match.get("text", ""))) for match in matches]
        if not pairs:
            return []
        
        scores = self.model.predict(pairs)
        scored = []
        for index, (match, score) in enumerate(zip(matches, scores)):
            row = dict(match)
            row["rerank_score"] = float(score)
            row["candidate_rank"] = index + 1
            scored.append(row)

        scored.sort(key=lambda item: (item["rerank_score"], item.get("score", 0)), reverse=True)
        return scored[:top_k]


def get_reranker() -> Reranker:
    global _reranker_provider_cache

    if _reranker_provider_cache is not None:
        return _reranker_provider_cache

    provider = settings.reranker_provider.lower()

    if provider == "keyword":
        _reranker_provider_cache = KeywordOverlapReranker()
        return _reranker_provider_cache

    if provider == "cross_encoder":
        _reranker_provider_cache = CrossEncoderReranker(model_name=settings.reranker_model)
        return _reranker_provider_cache

    raise ValueError(f"Unsupported reranker provider: {provider}")

def reset_reranker_cache() -> None:
    """
    Clear the reranker provider cache

    when monkeypatch setattr(), the cache should be cleared.
    """
    global _reranker_provider_cache
    _reranker_provider_cache = None

def load_reranker_model() -> Reranker:
    """
    Manually load reranker provider

    Function:
        Load the reranker provider instance in Swagger by clicking the button.
    """
    return get_reranker()

def unload_reranker_model() -> None:
    """
    Manually unload reranker provider

    Function:
        Unload the reranker provider instance in Swagger by clicking the button.
    """
    reset_reranker_cache()
    import gc
    gc.collect()
