from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.chunking import chunk_text
from app.embeddings import get_embedding_provider, load_embedding_model, unload_embedding_model
from app.generation import build_llm_answer
from app.ingestion import UnsupportedFileTypeError, extract_text
from app.storage import (
    get_document,
    init_db,
    insert_chunks,
    insert_document,
)
from app.vector_store import get_vector_store
from app.llm import LLMProviderError, load_ollama_model, unload_ollama_model, _llm_cache_flag
from app.rerank import load_reranker_model, unload_reranker_model, get_reranker
from app.config import settings


DATABASE_PATH = settings.database_path

class RetrievalFilters(BaseModel):
    source: str | None = None
    document_type: str | None = None

class RetrievalRequest(BaseModel):
    document_id: str
    question: str
    top_k: int = 3
    filters: RetrievalFilters | None = None

class AnswerRequest(BaseModel):
    document_id: str
    question: str
    top_k: int = 3
    filters: RetrievalFilters | None = None

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
        source="upload",
        document_type=extension.lstrip(".") or "unknown",
    )

    chunks = chunk_text(text)
    saved_chunks = insert_chunks(
        db_path=DATABASE_PATH,
        document_id=document["document_id"],
        chunks=chunks,
    )

    embedding_provider = get_embedding_provider() # load embedding model
    embedded_chunks = embedding_provider.embed_chunks(saved_chunks)
    for chunk in embedded_chunks:
        chunk["source"] = document["source"]
        chunk["document_type"] = document["document_type"]
    vector_store = get_vector_store()
    vector_store.upsert_embedding(embedded_chunks)
    
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

    embedding_provider = get_embedding_provider() # load embedding model
    query_embedding = embedding_provider.embed_text(request.question)
    vector_store = get_vector_store()

    filters = (
        request.filters.model_dump(exclude_none=True)
        if request.filters is not None
        else None
    )

    candidates_k = max(request.top_k*3, 10) # top_k -> candidate_k
    candidates = vector_store.search(
        document_id=request.document_id,
        query_embedding=query_embedding,
        top_k=candidates_k,
        filters=filters,
    )
    
    if _llm_cache_flag: # if llm model loaded, unload ollama model, or VRAM will be out of memory (my computer has 8GB VRAM)
        unload_ollama_model() 

    reranker = get_reranker() # after unload the ollama model
    matches = reranker.rerank(
        question=request.question,
        matches=candidates,
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
    if _llm_cache_flag: # if llm model loaded, release ollama model, give VRAM to reranker 
        unload_ollama_model() 

    retrieval_payload = retrieve(
        RetrievalRequest(
            document_id=request.document_id,
            question=request.question,
            top_k=request.top_k,
            filters=request.filters,
        )
    )
    try: 
        unload_reranker_model() # unload reranker model, or VRAM will be out of memory (my computer has 8GB VRAM)

        generated = build_llm_answer(
            question=request.question,
            matches=retrieval_payload["matches"],
        )
    except LLMProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "document_id": request.document_id,
        "question": request.question,
        "top_k": request.top_k,
        "answer": generated["answer"],
        "provider": generated["provider"],
        "sources": generated["sources"],
        "confidence_notes": generated["confidence_notes"],
    }


"""
@app.post("/admin/models/embedding/load")
def load_embedding_model_endpoint(status: int = 1) -> dict[str, str]:
    if status == 1:
        load_embedding_model()
        return {"status": "loaded", "model_type": "embedding"}
    elif status == 0:
        unload_embedding_model()
        return {"status": "unloaded", "model_type": "embedding"}


@app.post("/admin/models/reranker/load")
def load_reranker_model_endpoint(status: int = 1) -> dict[str, str]:
    if status == 1:
        load_reranker_model()
        return {"status": "loaded", "model_type": "rerank"}
    elif status == 0:
        unload_reranker_model()
        return {"status": "unloaded", "model_type": "rerank"}
    

@app.post("/admin/models/ollama/load")
def load_llm_model_endpoint(status: int = 1) -> dict[str, str]:
    if status == 1:
        load_ollama_model()
        return {"status": "loaded", "model_type": "ollama"}
    elif status == 0:
        unload_ollama_model()
        return {"status": "unloaded", "model_type": "ollama"}
"""