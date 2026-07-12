# Demo Transcript

## Environment

- Embedding provider: local BGE 
- Embedding model: BAAI\bge-small-zh-v1.5
- LLM provider: Ollama
- LLM model: qwen2.5:3b
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
eval/sample-personal-konwledge.md
```

Response:

```json
{
  "document_id": "doc_2ebe4beb3963",
  "filename": "sample-personal-konwledge.md",
  "extension": ".md",
  "status": "received",
  "chunk_count": 2
}
```

## Step 3: Retrivev

Request:

```json
{
  "document_id": "doc_2ebe4beb3963",
  "question": "What is the goal of this assistant?",
  "top_k": 3
}
```

Response notes:

- Top result should mention project goal.
- Scores are cosine similarity over stored chunk embeddings.

## Step 4: Answer

Request:

```json
{
  "document_id": "doc_2ebe4beb3963",
  "question": "What does the upload endpoint do?",
  "top_k": 3
}
```

Response notes:

- `sources` should include "extract text", "chunk text".
- Answer should stay grounded in uploaded document context.

### Answer:
The upload endpoint extracts text, chunks the text, stores chunk metadata in SQLite, and writes fake embeddings for local similarity search.\n\nSource chunk_id: chunk_c333859126c4
(Note: chunk_c333859126c4 is the top_1 chunk in the retrieval results.  In prompts.py, I ruled that "Mention the source chunk_id when useful.", so it mention the chunk in the answer.")

## Current Limitations

- Embeddings are still stored in SQLite JSON, not a vector database.
- PDF parsing is not implemented.
- Local Ollma answer speend depends on laptop hardware.
- Local BGE model is not optimized for performance.
- Evaluation set is small and manual.
