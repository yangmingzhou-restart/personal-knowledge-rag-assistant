from app.storage import (
    get_chunks_by_document,
    init_db,
    insert_chunks,
    insert_document,
    update_chunk_embedding,
)


def test_insert_and_get_chunks_by_document(tmp_path):
    db_path = tmp_path / "app.sqlite3"

    init_db(db_path)
    document = insert_document(
        db_path=db_path,
        filename="hello.txt",
        extension=".txt",
        size_bytes=9,
        status="received",
    )

    chunks = [
        {
            "chunk_index": 0,
            "text": "hello rag",
            "start_char": 0,
            "end_char": 9,
        },
        {
            "chunk_index": 1,
            "text": "rag storage",
            "start_char": 8,
            "end_char": 19,
        },
    ]

    inserted = insert_chunks(db_path, document["document_id"], chunks)
    saved = get_chunks_by_document(db_path, document["document_id"])

    assert len(inserted) == 2
    assert len(saved) == 2
    assert saved[0]["document_id"] == document["document_id"]
    assert saved[0]["chunk_index"] == 0
    assert saved[0]["text"] == "hello rag"
    assert saved[1]["chunk_index"] == 1


def test_update_chunk_embedding(tmp_path):
    db_path = tmp_path / "app.sqlite3"
    init_db(db_path)
    document = insert_document(
        db_path=db_path,
        filename="hello.txt",
        extension=".txt",
        size_bytes=20,
        status="received",
    )
    inserted = insert_chunks(
        db_path,
        document["document_id"],
        [
            {
                "chunk_index": 0,
                "text": "hello rag",
                "start_char": 0,
                "end_char": 9,
            }
        ],
    )

    update_chunk_embedding(db_path, inserted[0]["chunk_id"], [0.1, 0.2, 0.3])
    saved = get_chunks_by_document(db_path, document["document_id"])

    assert saved[0]["embedding"] == [0.1, 0.2, 0.3]
