from fastapi.testclient import TestClient

from app.generation import build_answer_stub, build_llm_answer
from app.llm import FakeLLMClient
from app.main import app


def test_build_answer_stub_uses_retrieved_chunks():
    matches = [
        {
            "chunk_id": "chunk_1",
            "document_id": "doc_1",
            "chunk_index": 0,
            "text": "RAG uses retrieved context.",
            "score": 0.9,
        }
    ]

    result = build_answer_stub("What does RAG use?", matches)

    assert "RAG uses retrieved context." in result["answer"]
    assert result["sources"][0]["chunk_id"] == "chunk_1"
    assert result["sources"][0]["score"] == 0.9
    assert "stub" in result["confidence_notes"]


def test_build_answer_stub_handles_empty_matches():
    result = build_answer_stub("unknown?", [])

    assert result["answer"] == "No relevant context was retrieved."
    assert result["sources"] == []
    assert "No chunks" in result["confidence_notes"]


def test_answer_returns_stub_answer_with_sources():
    client = TestClient(app)
    upload_response = client.post(
        "/upload",
        files={"file": ("hello.txt", b"RAG uses retrieved context.", "text/plain")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        "/answer",
        json={
            "document_id": document_id,
            "question": "What does RAG use?",
            "top_k": 2,
        },
    )

    payload = response.json()

    assert response.status_code == 200
    assert payload["document_id"] == document_id
    assert payload["question"] == "What does RAG use?"
    assert "answer" in payload
    assert len(payload["sources"]) >= 1
    assert "confidence_notes" in payload

def test_build_llm_answer_uses_prompt_and_llm_client():
    matches=[
        {
            "chunk_id": "chunk_1",
            "document_id": "doc_1",
            "chunk_index": 0,
            "text": "RAG uses retrieved context.",
            "score": 0.9,
        }
    ]

    result = build_llm_answer(
        question="What does RAG use?",
        matches=matches,
        llm_client=FakeLLMClient(),
    )

    assert "FAKE_ANSWER" in result["answer"]
    assert "RAG uses retrieved context." in result["answer"]
    assert result["provider"] == "fake"
    assert result["sources"][0]["chunk_id"] == "chunk_1"
    assert result["sources"][0]["score"] == 0.9
    assert "grounded prompt" in result["confidence_notes"]
