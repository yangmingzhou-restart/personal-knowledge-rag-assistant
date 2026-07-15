from abc import  ABC, abstractmethod

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
    
def get_reranker() -> Reranker:
    return KeywordOverlapReranker()
