# RAG Limitations

This project is a local portfolio RAG assistant, not a production-grade enterprise knowledge platform.

## Current Limits

- The default demo path uses SQLite-backed local storage. Qdrant is available as an optional VectorStore implementation, not the default production backend.
- Retrieval evaluation is intentionally small and anchor-based. It is useful for comparing changes, not for claiming broad benchmark performance.
- Local BGE embeddings, a cross-encoder reranker, and Ollama can exceed laptop VRAM if loaded together.
- PDF and DOCX text extraction is limited to machine-readable documents. OCR for scanned PDFs is future work.
- The project is currently single-user. It does not include account/password login, JWT, role/rank permissions, tenant isolation, or user-level document isolation.
- The project does not include production monitoring, rate limiting, audit logs, deployment hardening, or a complete frontend.

## Planned Improvements

- Add OCR fallback for scanned PDFs through the ingestion layer.
- Add authentication and user-level document isolation after the RAG portfolio version is stable.
- Add a lightweight UI only after the API, README, demo flow, and evaluation evidence are consistent.
- Add deployment and observability notes if the project is prepared for a hosted demo.

## Accurate Project Wording

Safe wording:

> This is a local RAG portfolio project with clear provider boundaries, retrieval evaluation, and a runnable API demo. It is not a production-grade multi-user system yet.

Avoid:

> Production-grade enterprise RAG platform with full authentication, OCR, and large-scale document support.
