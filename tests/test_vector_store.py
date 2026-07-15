from types import SimpleNamespace

import pytest

from app.vector_store import QdrantVectorStore, SQLiteVectorStore, get_vector_store
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


def test_qdrant_vector_store_upserts_chunk_payload(monkeypatch):
    calls = {"created": [], "upserted": []}

    class FakeQdrantClient:
        def __init__(self, url):
            self.url = url
            self.created = False

        def collection_exists(self, collection_name):
            return self.created

        def create_collection(self, collection_name, vectors_config):
            self.created = True
            calls["created"].append(
                {
                    "collection_name": collection_name,
                    "vector_size": vectors_config.size,
                }
            )

        def upsert(self, collection_name, points):
            calls["upserted"].append(
                {
                    "collection_name": collection_name,
                    "points": points,
                }
            )

    monkeypatch.setattr("qdrant_client.QdrantClient", FakeQdrantClient)

    store = QdrantVectorStore(
        url="http://127.0.0.1:6333",
        collection_name="test_chunks",
    )
    store.upsert_embedding(
        [
            {
                "chunk_id": "chunk_1",
                "document_id": "doc_1",
                "chunk_index": 0,
                "text": "hello rag",
                "start_char": 0,
                "end_char": 9,
                "created_at": "2026-07-14T00:00:00+00:00",
                "embedding": [1.0, 0.0],
            }
        ]
    )

    assert calls["created"][0]["collection_name"] == "test_chunks"
    assert calls["created"][0]["vector_size"] == 2
    point = calls["upserted"][0]["points"][0]
    assert point.vector == [1.0, 0.0]
    assert point.payload["chunk_id"] == "chunk_1"
    assert point.payload["text"] == "hello rag"


def test_qdrant_vector_store_search_returns_payload_with_score(monkeypatch):
    calls = {}

    class FakeQdrantClient:
        def __init__(self, url):
            self.url = url

        def collection_exists(self, collection_name):
            return True

        def query_points(self, **kwargs):
            calls.update(kwargs)
            return SimpleNamespace(
                points=[
                    SimpleNamespace(
                        payload={
                            "chunk_id": "chunk_1",
                            "document_id": "doc_1",
                            "chunk_index": 0,
                            "text": "hello rag",
                            "start_char": 0,
                            "end_char": 9,
                            "created_at": "2026-07-14T00:00:00+00:00",
                        },
                        score=0.88,
                    )
                ]
            )

    monkeypatch.setattr("qdrant_client.QdrantClient", FakeQdrantClient)

    store = QdrantVectorStore(
        url="http://127.0.0.1:6333",
        collection_name="test_chunks",
    )
    matches = store.search(
        document_id="doc_1",
        query_embedding=[1.0, 0.0],
        top_k=1,
    )

    assert calls["collection_name"] == "test_chunks"
    assert calls["query"] == [1.0, 0.0]
    assert calls["limit"] == 1
    assert matches == [
        {
            "chunk_id": "chunk_1",
            "document_id": "doc_1",
            "chunk_index": 0,
            "text": "hello rag",
            "start_char": 0,
            "end_char": 9,
            "created_at": "2026-07-14T00:00:00+00:00",
            "score": 0.88,
        }
    ]
