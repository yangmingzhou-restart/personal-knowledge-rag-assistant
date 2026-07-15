from fastapi.testclient import TestClient

from app.main import DATABASE_PATH, app
from app.storage import get_chunks_by_document


def test_upload_txt_file_returns_file_metadata():
    client = TestClient(app)

    response = client.post(
        "/upload",
        files={"file": ("hello.txt", b"hello rag", "text/plain")},
    )

    payload = response.json()
    saved_chunks = get_chunks_by_document(DATABASE_PATH, payload["document_id"])

    assert response.status_code == 200
    assert payload["document_id"].startswith("doc_")
    assert payload["filename"] == "hello.txt"
    assert payload["extension"] == ".txt"
    assert payload["size_bytes"] == 9
    assert payload["status"] == "received"
    assert payload["text_preview"] == "hello rag"
    assert payload["chunk_count"] == 1
    assert len(saved_chunks) == payload["chunk_count"]
    assert saved_chunks[0]["text"] == "hello rag"
    assert saved_chunks[0]["chunk_index"] == 0


def test_upload_txt_file_returns_200():
    client = TestClient(app)

    response = client.post(
        "/upload",
        files={"file": ("hello.txt", b"hello rag", "text/plain")},
    )

    assert response.status_code == 200


def test_upload_empty_file_returns_400():
    client = TestClient(app)
    response = client.post(
        "/upload",
        files={"file": ("empty.txt", b"", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty"


def test_upload_unsupported_file_type_returns_400():
    client = TestClient(app)
    response = client.post(
        "/upload",
        files={"file": ("demo.pdf", b"fake pdf content", "application/pdf")},
    )

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]
