# Personal Knowledge RAG Assistant

[![CI](https://github.com/yangmingzhou-restart/personal-knowledge-rag-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/yangmingzhou-restart/personal-knowledge-rag-assistant/actions/workflows/ci.yml)

## What This Project Does

A local FastAPI-based RAG assistant that can upload text-like files, parse content, split text into chunks, generate deterministic fake embeddings, retrieve relevant chunks, and return a deterministic answer stub with sources.

## Current Pipeline

```text
upload -> ingestion -> chunking -> embedding -> storage -> retrieval -> answer stub
```

## Tech Stack

- Python
- FastAPI
- SQLite
- pytest
- Deterministic fake embeddings

## Run Locally

```powershell
C:\Users\YangMingZhou\anaconda3\python.exe -m uvicorn app.main:app --reload
```

## API Demo

1. `GET /health`
2. `POST /upload`
3. `POST /retrieve`
4. `POST /answer`

## Interview Summary

This project demonstrates the core RAG pipeline with clear module boundaries, test coverage, and source-aware answer structure.

## Run with Docker

```powershell
docker build -t personal-knowledge-rag .
docker run --rm -p 8000:8000 personal-knowledge-rag
```

Open:

```text
https://127.0.0.1:8000/docs
```

## Current Limitations

- Embeddings are still stored in SQLite JSON, not a vector database.
- PDF parsing is not implemented.
- Local Ollma answer speend depends on laptop hardware.
- Local BGE model is not optimized for performance.
- Evaluation set is small and manual.

## Current Features

- Upload `.txt`, `.md`, and `.csv` files.
- Split uploaded text into traceable chunks.
- Store documents, chunks, and embeddings in SQLite.
- Generate local BGE embeddings.
- Retrieve top-k relevant chunks by cosine similarity.
- Generate grounded answers through a local Ollama LLM provider.
- Keep fake providers for tests and CI.

## Local Demo Stack

- API: FastAPI
- Metadata and chunk storage: SQLite
- Embedding model: BAAI/bge-base-zh-v1.5
- LLM provider: Ollama
- LLM model: qwen2.5:3b

## Configuration

Copy '.env.example' to '.env' and adjust local paths.

```env
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=D:\AI创业\AI模型\embedding-models\BAAI\bge-small-zh-v1.5
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:3b
```

## Limitations

- SQLite embedding search is acceptable for learning and demos but not a production vector database.
- Local LLM speed depends on available CPU/GPU memory.
- Current evaluation set is small and should be expanded before production claims.
