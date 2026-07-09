from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.chunking import chunk_text
from app.embeddings import get_embedding_provider
from app.generation import build_answer_stub
from app.ingestion import UnsupportedFileTypeError, extract_text
from app.retrieve import rank_chunks_by_similarity
from app.storage import (
    get_chunks_by_document,
    get_document,
    init_db,
    insert_chunks,
    insert_document,
    update_chunk_embedding,
)


DATABASE_PATH = Path("data/app.sqlite3")


class RetrievalRequest(BaseModel):
    document_id: str
    question: str
    top_k: int = 3


class AnswerRequest(BaseModel):
    document_id: str
    question: str
    top_k: int = 3


app = FastAPI(
    title="Personal Knowledge RAG Assistant",
    version="0.1.0",
)


@app.on_event("startup")
def startup() -> None:
    init_db(DATABASE_PATH)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str | int]:
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        text = extract_text(file.filename, content)
    except UnsupportedFileTypeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    extension = Path(file.filename or "").suffix.lower()
    document = insert_document(
        db_path=DATABASE_PATH,
        filename=file.filename or "",
        extension=extension,
        size_bytes=len(content),
        status="received",
    )

    chunks = chunk_text(text)
    saved_chunks = insert_chunks(
        db_path=DATABASE_PATH,
        document_id=document["document_id"],
        chunks=chunks,
    )

    embedding_provider = get_embedding_provider()
    embedded_chunks = embedding_provider.embed_chunks(saved_chunks)
    for chunk in embedded_chunks:
        update_chunk_embedding(
            db_path=DATABASE_PATH,
            chunk_id=chunk["chunk_id"],
            embedding=chunk["embedding"],
        )

    return {
        "document_id": document["document_id"],
        "filename": document["filename"],
        "extension": document["extension"],
        "size_bytes": document["size_bytes"],
        "status": document["status"],
        "text_preview": text[:120],
        "chunk_count": len(chunks),
    }


@app.post("/retrieve")
def retrieve(request: RetrievalRequest) -> dict:
    document = get_document(DATABASE_PATH, request.document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    if request.top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k must be greater than 0")

    chunks = get_chunks_by_document(DATABASE_PATH, request.document_id)
    embedding_provider = get_embedding_provider()
    query_embedding = embedding_provider.embed_text(request.question)
    matches = rank_chunks_by_similarity(
        query_embedding=query_embedding,
        chunks=chunks,
        top_k=request.top_k,
    )

    return {
        "document_id": request.document_id,
        "question": request.question,
        "top_k": request.top_k,
        "matches": matches,
    }


@app.post("/answer")
def answer(request: AnswerRequest) -> dict:
    retrieval_payload = retrieve(
        RetrievalRequest(
            document_id=request.document_id,
            question=request.question,
            top_k=request.top_k,
        )
    )

    generated = build_answer_stub(
        question=request.question,
        matches=retrieval_payload["matches"],
    )

    return {
        "document_id": request.document_id,
        "question": request.question,
        "top_k": request.top_k,
        "answer": generated["answer"],
        "sources": generated["sources"],
        "confidence_notes": generated["confidence_notes"],
    }
