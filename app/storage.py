import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                extension TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                text TEXT NOT NULL,
                start_char INTEGER NOT NULL,
                end_char INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                embedding_json TEXT,
                FOREIGN KEY (document_id) REFERENCES documents(document_id)
            )
            """
        )


def insert_document(
    db_path: Path,
    filename: str,
    extension: str,
    size_bytes: int,
    status: str,
) -> dict[str, str | int]:
    document = {
        "document_id": f"doc_{uuid4().hex[:12]}",
        "filename": filename,
        "extension": extension,
        "size_bytes": size_bytes,
        "status": status,
        "created_at": datetime.now(UTC).isoformat(),
    }

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO documents (
                document_id,
                filename,
                extension,
                size_bytes,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                document["document_id"],
                document["filename"],
                document["extension"],
                document["size_bytes"],
                document["status"],
                document["created_at"],
            ),
        )

    return document


def get_document(db_path: Path, document_id: str) -> dict[str, str | int] | None:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT
                document_id,
                filename,
                extension,
                size_bytes,
                status,
                created_at
            FROM documents
            WHERE document_id = ?
            """,
            (document_id,),
        ).fetchone()

    if row is None:
        return None

    return dict(row)


def insert_chunks(
    db_path: Path,
    document_id: str,
    chunks: list[dict[str, str | int]],
) -> list[dict[str, str | int]]:
    inserted = []
    created_at = datetime.now(UTC).isoformat()

    with sqlite3.connect(db_path) as conn:
        for chunk in chunks:
            row = {
                "chunk_id": f"chunk_{uuid4().hex[:12]}",
                "document_id": document_id,
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
                "start_char": chunk["start_char"],
                "end_char": chunk["end_char"],
                "created_at": created_at,
            }
            conn.execute(
                """
                INSERT INTO chunks (
                    chunk_id,
                    document_id,
                    chunk_index,
                    text,
                    start_char,
                    end_char,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["chunk_id"],
                    row["document_id"],
                    row["chunk_index"],
                    row["text"],
                    row["start_char"],
                    row["end_char"],
                    row["created_at"],
                ),
            )
            inserted.append(row)

    return inserted


def get_chunks_by_document(
    db_path: Path,
    document_id: str,
) -> list[dict[str, str | int]]:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT
                chunk_id,
                document_id,
                chunk_index,
                text,
                start_char,
                end_char,
                created_at,
                embedding_json
            FROM chunks
            WHERE document_id = ?
            """,
            (document_id,),
        ).fetchall()

    result = []
    for row in rows:
        item = dict(row)
        item["embedding"] = (
            json.loads(item["embedding_json"])
            if item["embedding_json"] is not None
            else None
        )
        del item["embedding_json"]
        result.append(item)

    return result


def update_chunk_embedding(
    db_path: Path,
    chunk_id: str,
    embedding: list[float],
) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE chunks
            SET embedding_json = ?
            WHERE chunk_id = ?
            """,
            (json.dumps(embedding), chunk_id),
        )
