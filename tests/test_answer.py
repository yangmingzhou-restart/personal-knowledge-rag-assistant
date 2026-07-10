from fastapi.testclient import TestClient

from app.main import app

def test_answer_returns_llm_answer_with_sources():
    with TestClient(app) as client:
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
    assert payload["provider"] == "fake"
    assert "FAKE_ANSWER" in payload["answer"]
    assert len(payload["sources"]) >= 1
