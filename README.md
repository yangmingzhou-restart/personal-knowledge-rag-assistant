# Personal Knowledge RAG Assistant

[![CI](https://github.com/yangmingzhou-restart/personal-knowledge-rag-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/yangmingzhou-restart/personal-knowledge-rag-assistant/actions/workflows/ci.yml)

## What This Project Does

A local FastAPI-based RAG assistant that uploads text-like files, extracts text, splits content into traceable chunks, stores metadata and embeddings in SQLite, retrieves relevant chunks, and generates grounded answers with source information.

## Current Pipeline

```text
upload -> ingestion -> chunking -> embedding -> storage -> retrieval -> prompt -> LLM answer
```

## Current Features

- Upload `.txt`, `.md`, and `.csv` files.
- Split uploaded text into chunks with `chunk_index`, `start_char`, and `end_char`.
- Store documents, chunks, and embedding JSON in SQLite.
- Use fake embedding and LLM providers for tests and GitHub Actions CI.
- Use local BGE embeddings for local demo retrieval.
- Retrieve top-k chunks by cosine similarity.
- Use a local Ollama LLM provider to generate grounded answers.
- Return `answer`, `provider`, `sources`, and `confidence_notes` from `/answer`.
- Centralize runtime configuration through `.env` and `BaseSettings`.

## Tech Stack

- Python
- FastAPI
- SQLite
- pytest
- sentence-transformers
- local BGE embedding model
- Ollama
- GitHub Actions

## API Endpoints

1. `GET /health`
2. `POST /upload`
3. `POST /retrieve`
4. `POST /answer`

## Local Demo Stack

- API: FastAPI
- Metadata and chunk storage: SQLite
- Embedding model: `BAAI/bge-small-zh-v1.5`
- LLM provider: Ollama
- LLM model: `qwen2.5:3b`

## Configuration

Copy `.env.example` to `.env` and adjust local paths.

```env
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=D:\AI创业\AI模型\embedding-models\BAAI\bge-small-zh-v1.5
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:3b
```

GitHub Actions CI should use fake providers and must not depend on local model files or a running Ollama service.

## Run Locally

Start Ollama first:

```powershell
D:\ollama\ollama.exe serve
```

Start the API:

```powershell
C:\Users\YangMingZhou\anaconda3\python.exe -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Run With Docker

Docker mode is mainly for API packaging verification. It does not automatically access Windows local model paths or the host Ollama service.

```powershell
docker build -t personal-knowledge-rag .
docker run --rm -p 8000:8000 personal-knowledge-rag
```

Open:

```text
http://127.0.0.1:8000/docs
```

For simple Docker verification, use fake providers:

```text
EMBEDDING_PROVIDER=fake
LLM_PROVIDER=fake
```

## Current Limitations

- Embeddings are stored in SQLite JSON instead of a dedicated vector database.
- Retrieval evaluation is still small and manual.
- The current retrieval stage does not include reranking.
- PDF and Word parsing are not fully implemented.
- The project is single-user and does not include authentication or user-level data isolation.
- Local LLM performance depends on laptop hardware.

## Planned Improvements

- Migrate vector storage to Qdrant, Milvus, or pgvector.
- Add a retrieval evaluation set with expected source chunks and top-k metrics.
- Add reranking after initial vector retrieval.
- Improve document parsing for PDF and Word files.
- Add authentication and user-level document isolation.

## Interview Summary

This project demonstrates a complete local RAG application workflow with clear module boundaries, source traceability, provider abstraction, CI-safe fake providers, and a local BGE + Ollama demo path.
