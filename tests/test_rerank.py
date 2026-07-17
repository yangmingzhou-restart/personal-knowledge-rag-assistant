import pytest

from app.rerank import KeywordOverlapReranker, CrossEncoderReranker

def test_keyword_overlap_rerank_moves_better_text_to_top():
    reranker = KeywordOverlapReranker()
    matches = [
        {"chunk_id": "generic", "text": "general project notes", "score": 0.9},
        {"chunk_id": "target", "text": "qdrant vector database integration", "score": 0.7},
    ]

    result = reranker.rerank(
        question="qdrant vector database",
        matches=matches,
        top_k=1,
    )

    assert result[0]["chunk_id"] == "target"
    assert result[0]["rerank_score"] == 3

def test_keyword_overlap_reranker_keeps_requested_top_k():
    reranker = KeywordOverlapReranker()
    matches = [
        {"chunk_id": "a", "text": "alpha"},
        {"chunk_id": "b", "text": "beta"},
    ]

    assert len(reranker.rerank("alpha beta", matches, top_k=1)) == 1

def test_keyword_overlap_rerank_rejects_invalid_top_k():
    reranker = KeywordOverlapReranker()

    with pytest.raises(ValueError):
        reranker.rerank("alpha beta", [], top_k=0)

def test_cross_encoder_rerank_scores_and_sorts(monkeypatch):
    class FakeCrossEncoder:
        def __init__(self, model_name: str):
            self.model_name = model_name
        
        def predict(self, pairs):
            return [0.1, 0.9]
        
    monkeypatch.setattr(
        "sentence_transformers.CrossEncoder",
        FakeCrossEncoder
    )
    reranker = CrossEncoderReranker("fake-reranker-model")
    result = reranker.rerank(
        question = "qdrant vector search",
        matches = [
            {"chunk_id": "low", "text": "general notes", "score": 0.8},
            {"chunk_id": "high", "text": "qdrant vector search", "score": 0.5},
        ],
        top_k=1,
    )

    assert result[0]["chunk_id"] == "high"
    