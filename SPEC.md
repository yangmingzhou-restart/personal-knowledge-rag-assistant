# LangChain-style 模块化 RAG 系统 Spec

## Purpose

Build a practical RAG application that lets users upload private documents and ask questions grounded in those documents.

This project should prove that the system can run a complete LLM application workflow, not just call a chatbot API.

The implementation follows a LangChain-style RAG workflow, but keeps the main RAG components implemented as explicit local modules rather than hiding the pipeline behind one framework call.

## User Story

As a user, I can upload documents and ask questions. The system answers using the uploaded content and shows which source chunks were used.

## Core Features

1. Upload `.txt`, `.md`, `.csv`, `.pdf`, and `.docx` files.
2. Extract plain text from uploaded files.
3. Split text into chunks of 500-800 Chinese/English characters.
4. Store document metadata in SQLite.
5. Store embeddings through a replaceable VectorStore boundary, with SQLite as the default local implementation and Qdrant as an optional local implementation.
6. Retrieve top-k relevant chunks for a question.
7. Generate an answer with source citations.
8. Return a JSON response containing `answer`, `sources`, and `confidence_notes`.

## Non-Goals

- Do not build user login in the current portfolio version.
- Do not build multi-tenant permission management in the current portfolio version.
- Do not build a complex frontend before the API works.
- Do not attempt fine-tuning.
- Do not claim enterprise production readiness.

## Architecture

```mermaid
flowchart LR
    A["User uploads document"] --> B["FastAPI upload endpoint"]
    B --> C["Text extraction"]
    C --> D["Chunking"]
    D --> E["Embedding"]
    E --> F["VectorStore boundary"]
    B --> G["SQLite metadata"]
    H["User question"] --> I["Question embedding"]
    I --> F
    F --> J["Top-k source chunks"]
    J --> K["Prompt assembly"]
    K --> L["LLM answer"]
    L --> M["Answer with citations"]
```

## API Endpoints

### GET `/health`

Purpose:
- Confirm the API service is running.

Output:

```json
{
  "status": "ok"
}
```

### POST `/upload`

Purpose:
- Upload and index one document.

Input:
- multipart file upload

Output:

```json
{
  "document_id": "doc_001",
  "filename": "example.pdf",
  "extension": ".pdf",
  "size_bytes": 12345,
  "status": "received",
  "text_preview": "Extracted text preview...",
  "chunk_count": 18
}
```

Validation:
- Reject unsupported extensions.
- Reject empty files.
- Return a clear error message if text extraction fails.

### POST `/retrieve`

Purpose:
- Inspect retrieval quality before answer generation.

Input:

```json
{
  "document_id": "doc_001",
  "question": "What are the main conclusions?",
  "top_k": 5
}
```

Output:

```json
{
  "document_id": "doc_001",
  "question": "What are the main conclusions?",
  "top_k": 5,
  "matches": [
    {
      "document_id": "doc_001",
      "chunk_id": "chunk_004",
      "chunk_index": 4,
      "score": 0.83,
      "text": "The key result is..."
    }
  ]
}
```

### POST `/answer`

Purpose:
- Ask a question and receive an answer grounded in retrieved document chunks.

Input:

```json
{
  "document_id": "doc_001",
  "question": "What are the main conclusions?",
  "top_k": 5
}
```

Output:

```json
{
  "document_id": "doc_001",
  "question": "What are the main conclusions?",
  "top_k": 5,
  "answer": "The document concludes that...",
  "provider": "fake",
  "sources": [
    {
      "chunk_id": "chunk_004",
      "chunk_index": 4,
      "score": 0.83,
      "text_preview": "The key result is..."
    }
  ],
  "confidence_notes": "The answer is grounded in 3 retrieved chunks."
}
```

## Data Model

### `documents`

Fields:
- `document_id`: stable document id.
- `filename`: uploaded filename.
- `extension`: file extension.
- `size_bytes`: uploaded file size.
- `created_at`: ingestion time.
- `status`: current API uses `received`.
- `source`: document source, currently usually `upload`.
- `document_type`: normalized document type, usually derived from the file extension.

### `chunks`

Fields:
- `chunk_id`: stable chunk id.
- `document_id`: parent document id.
- `chunk_index`: integer position in the document.
- `text`: chunk content.
- `created_at`: chunk creation time.

## Chunking Rules

Default:
- Chunk size: 700 characters.
- Overlap: 80 characters.

Rules:
- Preserve paragraph boundaries when possible.
- Fall back to character-based chunking for messy text.
- Skip whitespace-only chunks.
- Keep chunk ids deterministic: `doc_001_chunk_0001`.

## Embedding Rules

Development and CI mode:
- Use fake deterministic embeddings for tests and GitHub Actions.

Demo mode:
- Use a local BGE embedding model.

Principle:
- Keep embedding provider behind a small interface so the project can switch providers.

## Prompt Template

```text
You are a document question-answering assistant.
Answer only from the provided context.
If the context does not contain the answer, say that the uploaded documents do not provide enough evidence.
Always cite the source chunk ids used.

Question:
{question}

Context:
{retrieved_chunks}
```

## Evaluation Plan

Use the `eval/` folder:
- `eval/sample-personal-knowledge.md`
- `eval/evaluation-questions.md`
- expected evidence anchors
- anchor-based retrieval evaluation results, including baseline, fake reranker, and real reranker outputs

Evaluation table:

| Question | Expected Source | Retrieved Source | Pass | Notes |
|---|---|---|---|---|
| What is the main conclusion? | chunk_004 | chunk_004 | yes | Direct match |

Current small anchor-set result:

| Metric | Result |
|---|---:|
| Questions | 20 |
| Hit Rate@3 | 80% |
| Recall@3 | 80% |
| MRR | 0.6500 |
| Pass / Partial / Fail | 10 / 6 / 4 |

## Supported Project Claims

- Built a FastAPI-based modular RAG system with upload, parsing, chunking, embedding, retrieval, reranking, generation, and source citation.
- Supported `.txt`, `.md`, `.csv`, `.pdf`, and `.docx` ingestion for machine-readable documents.
- Designed replaceable provider boundaries for Embedding, VectorStore, Reranker, and LLM clients.
- Implemented SQLite as the default local vector storage path and Qdrant as an optional local VectorStore implementation.
- Added metadata filtering through `source` and `document_type` fields.
- Integrated local BGE embeddings, optional Cross-Encoder reranking, and Ollama-based local answer generation.
- Built deterministic fake providers so tests and GitHub Actions CI do not depend on local model files or running services.
- Created a 20-question anchor-based retrieval evaluation set with Hit Rate@K, Recall@K, MRR, and failure classification.
- Verified the local test suite with 81 automated tests passing in the current closeout state.
