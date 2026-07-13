import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


def init_db(db_path: Path) -> None:
    """
    db_path: Path, 数据库路径

    return: None. 初始化数据库，创建documents和chunks表
    """
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
    """
    db_path: Path, 数据库路径
    filename: str, 文档的文件名
    extension: str, 文档的扩展名
    size_bytes: int, 文档的大小（字节）
    status: str, 文档的状态（如"received"、"processed"等）

    return: dict[str, str | int], 
            文档的详细信息，包含文档id、文件名、扩展名、大小、状态、创建时间等
            {
                "document_id": "doc_1234567890",
                "filename": "example.pdf",
                "extension": "pdf",
                "size_bytes": 1024,
                "status": "received",
                "created_at": "2023-01-01T00:00:00+00:00",
            }
    """    
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
    """
    db_path: Path, 数据库路径
    document_id: str, 要查找的文档id

    return: dict[str, str | int] | None, 
            文档信息或None。该文档对应的第一条数据,最在于验证这个文档在于验证这个文档是否存在于数据库中
            如果返回None，则API层抛出404错误码，提示文档不存在
            {
                "document_id": "doc_1234567890",
                "filename": "example.pdf",
                "extension": "pdf",
                "size_bytes": 1024,
                "status": "received",
                "created_at": "2023-01-01T00:00:00+00:00",
            }
    """
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
    """
    db_path: Path, 数据库路径
    document_id: str, 要插入的文档id
    chunks: list[dict[str, str | int]], 要插入的chunk列表
            {
                "chunk_index": 0,
                "text": "Hello, world!",
                "start_char": 0,
                "end_char": 11,
            }

    return: list[dict[str, str | int]], 
            一个chunks，包含所有插入的chunk
            [
                {
                    "chunk_id": "chunk_1234567890",
                    "document_id": "doc_1234567890",
                    "chunk_index": 0,
                    "text": "Hello, world!",
                    "start_char": 0,
                    "end_char": 11,
                    "created_at": "2023-01-01T00:00:00+00:00",
                }
            ]
    """
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
    """
    db_path: Path, 数据库路径
    document_id: str, 要查找的文档id

    return: list[dict[str, str | int]], 
            一个chunks，包含所有源于该文档的chunk
            [
                {
                    "chunk_id": "chunk_1234567890",
                    "document_id": "doc_1234567890",
                    "chunk_index": 0,
                    "text": "Hello, world!",
                    "start_char": 0,
                    "end_char": 11,
                    "created_at": "2023-01-01T00:00:00+00:00",
                    "embedding": None,
                }
            ]
    """
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
    """
    db_path: Path, 数据库路径
    chunk_id: str, 要更新的chunkid
    embedding: list[float], 要更新的chunk的embedding
               [0.79, 0.34, 0.3, ...]

    return: None. 
    作用：把 embedding 序列化为 JSON 字符串，写入 chunks.embedding_json。
    后续 get_chunks_by_document() 会再把 embedding_json 解析回 list[float]。
    """
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE chunks
            SET embedding_json = ?
            WHERE chunk_id = ?
            """,
            (json.dumps(embedding), chunk_id),
        )
