from fastapi.testclient import TestClient

from app.main import app
from app.retrieve import cosine_similarity, rank_chunks_by_similarity


def test_cosine_similarity_returns_one_for_same_vector():
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0


def test_cosine_similarity_returns_zero_for_orthgonal_vectors():
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0


def test_rank_chunks_by_similarity_returns_top_k():
    query_embedding = [1.0, 0.0]
    chunks = [
        {"chunk_id": "chunk_low", "text": "low", "embedding": [0.0, 1.0]},
        {"chunk_id": "chunk_high", "text": "high", "embedding": [1.0, 0.0]},
    ]

    results = rank_chunks_by_similarity(query_embedding, chunks, top_k=1)

    assert len(results) == 1
    assert results[0]["chunk_id"] == "chunk_high"
    assert results[0]["score"] == 1.0


def test_rank_chunks_skips_chunks_without_embedding():
    query_embedding = [1.0, 0.0]
    chunks = [
        {"chunk_id": "missing", "text": "missing", "embedding": None},
        {"chunk_id": "valid", "text": "valid", "embedding": [1.0, 0.0]},
    ]

    results = rank_chunks_by_similarity(query_embedding, chunks, top_k=5)

    assert len(results) == 1
    assert results[0]["chunk_id"] == "valid"


def test_invalid_top_k_raises_value_error():
    try:
        rank_chunks_by_similarity([1.0], [], top_k=0)
    except ValueError as exc:
        assert "top_k" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_retrieve_returns_matching_chunks():
    client = TestClient(app)
    upload_response = client.post(
        "/upload",
        files={"file": ("hello.txt", b"hello rag retrieval", "text/plain")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        "/retrieve",
        json={
            "document_id": document_id,
            "question": "hello rag",
            "top_k": 2,
        },
    )

    payload = response.json()

    assert response.status_code == 200
    assert payload["document_id"] == document_id
    assert payload["question"] == "hello rag"
    assert payload["top_k"] == 2
    assert len(payload["matches"]) >= 1


def test_retrieve_unknown_document_returns_404():
    client = TestClient(app)

    response = client.post(
        "/retrieve",
        json={
            "document_id": "doc_missing",
            "question": "hello",
            "top_k": 3,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_retrieve_invalid_top_k_returns_400():
    client = TestClient(app)
    upload_response = client.post(
        "/upload",
        files={"file": ("hello.txt", b"hello rag retrieval", "text/plain")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        "/retrieve",
        json={
            "document_id": document_id,
            "question": "hello",
            "top_k": 0,
        },
    )

    assert response.status_code == 400
    assert "top_k" in response.json()["detail"]

def test_retrieve_matches_include_similarity_score():
    client = TestClient(app)
    upload_response = client.post(
        "/upload",
        files={"file": ("hello.txt", b"hello rag retrieval", "text/plain")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        "/retrieve",
        json={
            "document_id": document_id,
            "question": "your question",
            "top_k": 1,
        },
    )

    assert response.status_code == 200
    match = response.json()["matches"][0]
    assert "score" in match
    assert "chunk_id" in match

def test_retrieve_matcges_include_rerank_metadata():
    client = TestClient(app)
    upload_response = client.post(
        "/upload",
        files={"file": ("hello.txt", b"hello rag retrieval", "text/plain")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        "/retrieve",
        json={
            "document_id": document_id,
            "question": "hello rag",
            "top_k": 1,
        },
    )

    assert response.status_code == 200

    match = response.json()["matches"][0]
    assert "score" in match
    assert "rerank_score" in match
    assert "candidate_rank" in match
