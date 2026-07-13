import pytest

from app.vector_store import SQLiteVectorStore, get_vector_store
from app.config import settings

def test_sqlite_vector_store_upserts_embeddings(monkeypatch, tmp_path):
    calls = []

    def fake_update_chunk_embedding(db_path, chunk_id, embedding):
        calls.append(
            {
                "db_path": db_path,
                "chunk_id": chunk_id,
                "embedding": embedding,
            }
        )
    
    monkeypatch.setattr(
        "app.vector_store.update_chunk_embedding",
        fake_update_chunk_embedding,
    )
    
    store = SQLiteVectorStore(tmp_path / "test.sqlite3")
    store.upsert_embedding(
        [
            {"chunk_id": "chunk_1", "embedding": [1.0, 0.0]},
            {"chunk_id": "chunk_2", "embedding": [0.0, 1.0]},
        ]
    )

    assert [call["chunk_id"] for call in calls] == ["chunk_1", "chunk_2"]
    assert calls[0]["embedding"] == [1.0, 0.0]

def test_sqlite_vector_store_rejects_chunk_without_embedding(tmp_path):
    store = SQLiteVectorStore(tmp_path / "test.sqlite3")
    with pytest.raises(ValueError, match="chunk embedding is required"):
        store.upsert_embedding(
            [
                {"chunk_id": "chunk_1"} #没有"embedding"
            ]
        )

def test_sqlite_vector_store_search_ranks_chunks(monkeypatch, tmp_path):
    chunks = [
        {
            "chunk_id": "chunk_1",
            "document_id": "doc_1",
            "chunk_index": 0,
            "text": "Python RAG retrieval",
            "embedding": [1.0, 0.0],
        },
        {
            "chunk_id": "chunk_2",
            "document_id": "doc_1",
            "chunk_index": 1,
            "text": "unrelated note",
            "embedding": [0.0, 1.0],
        },
    ]
    
    def fake_get_chunks_by_document(db_path, document_id):
        assert document_id == "doc_1"
        return chunks
    
    monkeypatch.setattr(
        "app.vector_store.get_chunks_by_document",
        fake_get_chunks_by_document,
    )
    
    store = SQLiteVectorStore(tmp_path / "test.sqlite3")
    matches = store.search(
        document_id="doc_1",
        query_embedding=[1.0, 0.0],
        top_k=1,
    )
    
    assert len(matches) == 1
    assert matches[0]["chunk_id"] == "chunk_1"
    assert matches[0]["score"] == 1.0

def test_get_vector_store_defaults_to_sqlite(monkeypatch):
    monkeypatch.setattr(settings, "vector_store_provider", "sqlite")
    
    vector_store = get_vector_store()
    
    assert isinstance(vector_store, SQLiteVectorStore)

def test_get_vector_store_rejects_unknown_provider(monkeypatch):
    monkeypatch.setattr(settings, "vector_store_provider", "unknown")

    try:
        get_vector_store()
    except ValueError as exc:
        assert "Unsupported vector store provider: unknown" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
