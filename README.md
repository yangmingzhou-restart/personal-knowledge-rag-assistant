# Personal Knowledge RAG Assistant

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

## Known Limitations

- Fake embeddings are not semantic embeddings.
- Answer generation is a deterministic stub, not a real LLM.
- No vector database yet.
- No authentication or production deployment yet.

## Interview Summary

This project demonstrates the core RAG pipeline with clear module boundaries, test coverage, and source-aware answer structure.

## Run with Docker

'''powershell
docker build -t personal-knowledge-rag .
docker run --rm -p 8000:8000 personal-knowledge-rag
'''

Open:

'''text
https://127.0.0.1:8000/docs
'''