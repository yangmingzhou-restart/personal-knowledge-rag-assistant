# Project Audit

## Audit Date

2026-07-13

## Current Project Status

The project is a local RAG assistant suitable for portfolio demonstration and  interview discussion.

It currently supports:

- FastAPI API service.
- File upload for `.txt`, `.md`, and `.csv`.
- Text extraction and chunking.
- SQlite storage for documents, chunks and embedding JSON.
- Fake embedding provider for test and CI.
- Local BGE embedding provider for local demo.
- Top-k retrieval by cosine similarity.
- Fake LLM provider for tests and CI.
- Ollama LLM provider for local answer generation.
- `/retrieval` and `/answer` endpoints with source-aware output.

## Current Boundaries

- PDF and Word parsing are not fully implemented.
- No dedicated vector database yet.
- No reranking stage yet. 
- Retrieval evaluation is still small and manual.
- No authentication or user-level data isolation.

## Code Inventory

Expected core modules:

- `app/main.py`: FastAPI endpoints and request models.
- `app/ingestion.py`: file text extraction.
- `app/chunking.py`: text chunking,
- `app/storage.py`: SQLite documents/chunks/embeddings.
- `app/retrieve.py`: similarity ranking.
- `app/prompts.py`: grounded prompt construction.
- `app/generation.py`: answer-building boundary.
- `app/llm.py`: fake and Ollama LLM clients.
- `app/config.py`: `BaseSettings` configuration.

Manual check result:

- [ ] All expected modules exist.
- [ ] No module name contradicts its responsibility.
- [ ] API layer does not contain provider-specific model logic.
- [ ] Tests do not require private local model paths by default.

## Test Audit

Local command:

```powershell
C:\Users\YangMingZhou\anaconda3\python.exe -m pytest -q
```

Result:

- [ ] Passed locally.
- [ ] If failed, record the failing test and reason.

CI rules:

- CI should use fake providers.
- CI should not require local BGE model files.
- CI should not require a running Ollama services.
- CI should not depend on private '.env'.

Tests that really load local models or call a real service should be marked separately and skipped in CI.

## Documentation Consistency Audit

Check these files:

- `README.md`
- `docs/demo-flow.md`
- `docs/demo-transcript.md`
- `.env.example`

Search for overclaims:

```powershell
Select-String -Path README.md, docs\*.md -Pattern "production vector|full PDF|answer stub|deterministic fake|Project 2|multi-user"
```

Rules:

- If README says a feature exists, code must support it.
- If demo-flow gives a command, the command must be runnable.
- If demo-transcript gives an answer, it must be marked as example or copied from a real run.
- Limitations should be honest but paired with planned improvements.

## GitHub Cleanup Checklist

- [ ] `git status -sb` has only intended files.
- [ ] `.env` is not tracked.
- [ ] `.env.example` is tracked.
- [ ] `data/*.sqlite3` or generated local databases are not committed unless explicitly intended.
- [ ] `.pytest_cache`, `__pycache__`, and local model files are not committed.
- [ ] README badge points to the correct workflow.
- [ ] docs explain local model requirements.

## Commit Plan

Recommended split:

1. Documentation alignment commit.
2. Test/CI fix commit, only if code or tests changed.
3. Career-material commit, if those files are inside a tracked repo.