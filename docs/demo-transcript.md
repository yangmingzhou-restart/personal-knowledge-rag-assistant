# Demo Transcript

## Environment

- Embedding provider: local BGE
- Embedding model: `BAAI/bge-small-zh-v1.5`
- LLM provider: Ollama
- LLM model: `qwen2.5:3b`
- API port: 8000

## Step 1: Health Check

Request:

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

## Step 2: Upload Document

Endpoint:

```http
POST /upload
```

Uploaded file:

```text
eval/sample-personal-knowledge.md
```

Example response:

```json
{
  "document_id": "doc_2ebe4beb3963",
  "filename": "sample-personal-knowledge.md",
  "extension": ".md",
  "status": "received",
  "chunk_count": 2
}
```

## Step 3: Retrieve

Request:

```json
{
  "document_id": "doc_2ebe4beb3963",
  "question": "What does the upload endpoint do?",
  "top_k": 3
}
```

Expected checks:

- Top matches should mention text extraction, chunking, metadata storage, or embeddings.
- Scores are cosine similarity over stored chunk embeddings.
- Inspect retrieval before judging the final answer quality.

## Step 4: Answer

Request:

```json
{
  "document_id": "doc_2ebe4beb3963",
  "question": "What does the upload endpoint do?",
  "top_k": 3
}
```

Expected checks:

- `provider` should be `ollama:qwen2.5:3b` in local Ollama mode.
- `sources` should include retrieved chunk ids.
- The answer should stay grounded in uploaded document context.

Example answer summary:

```text
The upload endpoint extracts text from the uploaded file, splits the text into chunks, stores document and chunk metadata in SQLite, and writes embeddings for retrieval.
```

## Current Limitations

- The default local path uses SQLite-backed vector storage, while Qdrant is available behind the VectorStore boundary.
- Retrieval evaluation is small and anchor-based, with metrics such as Hit Rate@K, Recall@K, and MRR.
- PDF and Word text extraction is supported for machine-readable documents; OCR for scanned PDFs is not implemented.
- The project is single-user and does not include authentication or user-level data isolation.
- Local LLM performance depends on laptop hardware.
