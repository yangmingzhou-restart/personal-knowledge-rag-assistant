# Retrieval Evaluation Results

Model:
- Embedding provider: local
- Model path: D:\AI创业\AI模型\embedding-models\BAAI\bge-small-zh-v1.5
- Storage: SQLite chunk embeddings

Document:
- File: eval/sample-personal-konwledge.md
- document_id: doc_ec038f9eb530

## Summary

| Metric | Result |
|---|---|
| Total questions |  |
| Pass |  |
| Partial pass |  |
| Fail |  |

## Detailed Results

### Q1

Question: What is the goal of this assistant?

Expected source: Project Goal

Top-1 result:

"# Personal Knowledge Sample\r\n\r\n## Project Goal\r\n\r\nThe Personal Knowledge RAG Assistant helps a user upload notes, split them into chunks, retrieve relevant context, and generate grounded answers.\r\n\r\n## Architecture\r\n\r\nThe upload endpoint extracts text, chunks the text, stores chunk metadata in SQLite, and writes fake embeddings for local similarity search.\r\n\r\n## Retrieval\r\n\r\nThe retrieval endpoint receives a document_id, question, and top_K. It embeds the question, compares it with stored chunk"

Top-3 contains expected source: yes/no

no, the retrieved chunks indicates how the project test works.
"t project uses fake embeddings and a fake LLM client. This keeps tests stable but does not measure real semantic retrieval quality.\r\n"

Judgment: pass / partial pass / fail

partial pass

Reason:

top_k = 3, the top_1 retrieval is good, but the top_3 is not relevant with the question.
Besides, the ranks is reasonanble, the top_1 is indeed the expected source.
