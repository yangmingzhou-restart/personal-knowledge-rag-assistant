# LangChain-style 模块化 RAG 系统

[![CI](https://github.com/yangmingzhou-restart/personal-knowledge-rag-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/yangmingzhou-restart/personal-knowledge-rag-assistant/actions/workflows/ci.yml)

## What This Project Does

A local FastAPI-based, LangChain-style RAG assistant that uploads text-like files, extracts text, splits content into traceable chunks, stores metadata and embeddings, retrieves relevant chunks through a replaceable VectorStore boundary, reranks candidate chunks, and generates grounded answers with source information.

This repository does not depend on LangChain as the core framework. "LangChain-style" means the project follows the common RAG application pattern: ingestion, chunking, embedding, vector retrieval, reranking, prompt assembly, LLM generation, and source citation.

## Current Pipeline

```mermaid
flowchart LR
    A["Upload"] --> B["Ingestion"]
    B --> C["Chunking"]
    C --> D["Embedding Provider"]
    D --> E["VectorStore Boundary"]
    E --> F["Reranker Provider"]
    F --> G["Grounded Prompt"]
    G --> H["LLM Provider"]
    H --> I["Answer + Sources"]
```

## Current Features

- Upload `.txt`, `.md`, `.csv`, `.pdf`, and `.docx` files.
- Extract machine-readable PDF and Word text, while keeping OCR as a planned improvement.
- Split uploaded text into chunks with `chunk_index`, `start_char`, and `end_char`.
- Store documents, chunks, and embedding JSON in SQLite.
- Use fake embedding and LLM providers for tests and GitHub Actions CI.
- Use local BGE embeddings for local demo retrieval.
- Retrieve top-k chunks by cosine similarity.
- Filter retrieval by metadata fields such as `source` and `document_type`.
- Use a deterministic keyword reranker for CI and an optional local Cross-Encoder reranker for real local demos.
- Use a local Ollama LLM provider to generate grounded answers.
- Return `answer`, `provider`, `sources`, and `confidence_notes` from `/answer`.
- Centralize runtime configuration through `.env` and `BaseSettings`.
- Use a replaceable `VectorStore` boundary with SQLite as the default local implementation.
- Keep Qdrant as an optional vector store implementation for local experiments.
- Rerank retrieved candidates before returning final top-k matches.
- Evaluate retrieval quality with anchor-based metrics such as Hit Rate@K, Recall@K, and MRR.

## Tech Stack

- Python
- FastAPI
- SQLite
- pytest
- sentence-transformers
- local BGE embedding model
- Ollama
- GitHub Actions
- Qdrant client
- cross-encoder reranker
- provider-based architecture

## API Endpoints

1. `GET /health`
2. `POST /upload`
3. `POST /retrieve`
4. `POST /answer`

## Local Demo Stack

- API: FastAPI
- Metadata and chunk storage: SQLite
- Default vector store: SQLite
- Optional vector store: Qdrant
- Embedding model: `BAAI/bge-small-zh-v1.5`
- Reranker model: `BAAI/bge-reranker-base` 
- LLM provider: Ollama
- LLM model: `qwen2.5:3b`

## Configuration

Copy `.env.example` to `.env` and adjust local paths.

```env
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=D:\models\embedding-models\BAAI\bge-small-zh-v1.5

RERANKER_PROVIDER=cross_encoder
RERANKER_MODEL=D:\models\rerank-model\BAAI\bge-reranker-base

VECTOR_STORE_PROVIDER=sqlite
QDRANT_URL=http://127.0.0.1:6333
QDRANT_COLLECTION=personal_knowledge_chunks

LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:3b
```

GitHub Actions CI should use fake providers and must not depend on local model files or a running Ollama service: `EMBEDDING_PROVIDER=fake`, `RERANKER_PROVIDER=keyword`, `LLM_PROVIDER=fake`, `VECTOR_STORE_PROVIDER=sqlite`.

## Current Limitations

- The default local demo still uses SQLite-backed vector storage; Qdrant is available as a replaceable implementation but is not the default production backend.
- Retrieval evaluation is intentionally small and anchor-based; it is useful for comparing changes, not a comprehensive benchmark.
- Real embedding, reranker, and Ollama models can exceed laptop VRAM if loaded together, so local demos may require manual model loading/unloading.
- PDF and Word text extraction is supported for machine-readable documents; OCR for scanned PDFs is not implemented.
- The project is single-user and does not include authentication, authorization, or user-level data isolation.
- The project is not a production-grade RAG platform; it is a local portfolio project focused on RAG architecture, provider boundaries, evaluation, and demoability.

## Evaluation

The project includes an anchor-based retrieval evaluation set under `eval/`.

The latest local evaluation can run through the reranker stage and report:

- Hit Rate@K
- Recall@K
- MRR
- pass / partial / fail cases

This makes retrieval quality comparable across changes such as reranking, metadata filters, and vector store implementations.

Latest small anchor-set result:

| Metric | Result |
|---|---:|
| Questions | 20 |
| Hit Rate@3 | 80% |
| Recall@3 | 80% |
| MRR | 0.6500 |
| Pass / Partial / Fail | 10 / 6 / 4 |

This is a small project evaluation set, not a public benchmark.

See:

- `eval/evaluation-questions.md`
- `eval/evaluation-results-real-reranker.md`
- `eval/run_retrieval_evaluation.py`

## Planned Improvements

- Add OCR fallback for scanned PDFs.
- Add authentication and user-level document isolation.
- Add a lightweight web UI and deployment hardening after the RAG portfolio version is stable.
