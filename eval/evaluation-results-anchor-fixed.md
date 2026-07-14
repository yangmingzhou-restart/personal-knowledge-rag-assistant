# Retrieval Evaluation Results

Date: 2026-07-14T06:11:33.739994+00:00
Sample document: `D:\AI创业\找工作\ai-rag-agent-learning-system\generated\portfolio\personal-knowledge-rag\eval\sample-personal-knowledge.md`
Document ID: doc_969a74f61a0f
Chunk size: 500
Overlap: 50
Top k: 3

## Summary

| Metric | Result |
| --- | --- |
| Total questions | 20 |
| Pass | 7 |
| Partial | 4 |
| Fail | 9 |

## Detailed Results

| ID | Question | Expected anchor | Top-1 anchor | Top-1 evidence | Top-3 anchors | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | What is the  main purpose of the Personal Knowledge RAG Assistant? | `[ANCHOR-PROJECT-PURPOSE]` | `unknown / no anchor` | # Personal Knowledge RAG Evaluation Sample This document is intentionally longer than a normal quick demo note. With the current chunking se | unknown / no anchor | unknown / no anchor | [ANCHOR-PROJECT-PURPOSE] | partial |  |
| Q2 | What happens after a user uploads a file? | `[ANCHOR-UPLOAD-PIPELINE]` | `[ANCHOR-UPLOAD-PIPELINE]` | g, prompt construction, and LLM provider boundaries. The goal is not to build a perfect enterprise system immediately. The goal is to build  | [ANCHOR-UPLOAD-PIPELINE] | [ANCHOR-PROMPT-BUILDER] | unknown / no anchor | pass |  |
| Q3 | What should the chunking module be responsible for? | `[ANCHOR-CHUNKING-POLICY]` | `unknown / no anchor` | hallucination risk, although it does not eliminate it completely. The prompt should preserve source information such as chunk_id, chunk_inde | unknown / no anchor | [ANCHOR-CHUNKING-POLICY] | unknown / no anchor | partial |  |
| Q4 | Why does get_chunks_by_document convert embedding_json back into a list of floats? | `[ANCHOR-STORAGE-LAYER]` | `[ANCHOR-EMBEDDING-PROVIDER]` | and converts embedding_json back into a Python list of floats. This conversion is important because retrieval code expects embeddings as lis | [ANCHOR-EMBEDDING-PROVIDER] | unknown / no anchor | [ANCHOR-PROMPT-BUILDER] | fail |  |
| Q5 | Why does the project use an EmbeddingProvider boundary? | `[ANCHOR-EMBEDDING-PROVIDER]` | `unknown / no anchor` | ed answers. The project is not a generic chatbot. Its main value is that answers should be connected to uploaded source material. The system | unknown / no anchor | unknown / no anchor | [ANCHOR-PROJECT-PURPOSE] | fail |  |
| Q6 | Why should the local BGE embedding model not be loaded on every request? | `[ANCHOR-EMBEDDING-PROVIDER]` | `unknown / no anchor` | t does not represent real semantic similarity, but it makes tests stable and fast. LocalEmbeddingProvider uses a sentence-transformers model | unknown / no anchor | unknown / no anchor | unknown / no anchor | fail |  |
| Q7 | Why should main.py use get_vector_store instead of directly importing SQLiteVectorStore? | `[ANCHOR-VECTOR-STORE]` | `unknown / no anchor` | ging the API endpoint shape. The API should ask for a vector store through get_vector_store rather than directly importing a concrete implem | unknown / no anchor | [ANCHOR-METADATA-FILTER] | [ANCHOR-VECTOR-STORE] | partial |  |
| Q8 | How are chunks ranked during retrieval? | `[ANCHOR-RETRIEVAL-RANKING]` | `unknown / no anchor` | ss embeds the user question and compares the query embedding with stored chunk embeddings. The ranking function uses cosine similarity. A hi | unknown / no anchor | unknown / no anchor | [ANCHOR-RERANKING-PLAN] | fail |  |
| Q9 | Why does one chunk have one embedding vector instead of one vector per character? | `[ANCHOR-RETRIEVAL-RANKING]` | `unknown / no anchor` | ss embeds the user question and compares the query embedding with stored chunk embeddings. The ranking function uses cosine similarity. A hi | unknown / no anchor | unknown / no anchor | [ANCHOR-CHUNKING-POLICY] | fail |  |
| Q10 | What does the grounded prompt builder do? | `[ANCHOR-PROMPT-BUILDER]` | `[ANCHOR-PROMPT-BUILDER]` | That may require better chunking, better documents, better embeddings, metadata filters, or query rewriting. ## Section 08 - Grounded Prompt | [ANCHOR-PROMPT-BUILDER] | unknown / no anchor | unknown / no anchor | pass |  |
| Q11 | How should the project handle an Ollama provider failure? | `[ANCHOR-LLM-CLIENT]` | `unknown / no anchor` | ed answers. The project is not a generic chatbot. Its main value is that answers should be connected to uploaded source material. The system | unknown / no anchor | unknown / no anchor | [ANCHOR-PROJECT-PURPOSE] | fail |  |
| Q12 | What should the answer endpoint return besides the final answer? | `[ANCHOR-ANSWER-ENDPOINT]` | `[ANCHOR-ANSWER-ENDPOINT]` | not leak private details or raw stack traces to the user. A stable API should return a clear error message and status code while keeping int | [ANCHOR-ANSWER-ENDPOINT] | unknown / no anchor | unknown / no anchor | pass |  |
| Q13 | What is the relationship between .env, config.py, and settings? | `[ANCHOR-CONFIG-ENV]` | `[ANCHOR-CONFIG-ENV]` | ibility is central to a RAG application. Without sources, the user cannot easily inspect whether the model answer is actually grounded. ## S | [ANCHOR-CONFIG-ENV] | unknown / no anchor | [ANCHOR-PROMPT-BUILDER] | pass |  |
| Q14 | Why should CI use fake providers by default? | `[ANCHOR-TESTING-CI]` | `unknown / no anchor` | er is fake or real. It should only call a common generate method. The Ollama client sends a POST request to the local Ollama API. It uses a  | unknown / no anchor | [ANCHOR-PROMPT-BUILDER] | unknown / no anchor | fail |  |
| Q15 | How should retrieval evaluation classify pass, partial, and fail? | `[ANCHOR-RETRIEVAL-EVALUATION]` | `[ANCHOR-RETRIEVAL-EVALUATION]` | l evaluation can record real retrieval quality in markdown files, while CI checks basic structure and core deterministic behavior. ## Sectio | [ANCHOR-RETRIEVAL-EVALUATION] | unknown / no anchor | unknown / no anchor | pass |  |
| Q16 | When is reranking most useful in this project? | `[ANCHOR-RERANKING-PLAN]` | `unknown / no anchor` | ed answers. The project is not a generic chatbot. Its main value is that answers should be connected to uploaded source material. The system | unknown / no anchor | [ANCHOR-PROJECT-LIMITATIONS] | unknown / no anchor | fail |  |
| Q17 | What is the intended first step for adding Qdrant? | `[ANCHOR-QDRANT-PLAN]` | `[ANCHOR-QDRANT-PLAN]` | r measurable benefit. ## Section 15 - Qdrant Plan [ANCHOR-QDRANT-PLAN] Qdrant is a vector database that can store vectors and perform simila | [ANCHOR-QDRANT-PLAN] | unknown / no anchor | [ANCHOR-RERANKING-PLAN] | pass |  |
| Q18 | Why is metadata filtering needed beyond document_id retrieval? | `[ANCHOR-METADATA-FILTER]` | `[ANCHOR-METADATA-FILTER]` | an [ANCHOR-METADATA-FILTER] Single document_id retrieval is useful for learning, but it is limited. Real knowledge bases often search across | [ANCHOR-METADATA-FILTER] | [ANCHOR-RETRIEVAL-RANKING] | [ANCHOR-PROJECT-LIMITATIONS] | pass |  |
| Q19 | What limitations should be honestly stated about the current project? | `[ANCHOR-PROJECT-LIMITATIONS]` | `unknown / no anchor` | practical AI application engineering without pretending that every production concern is solved. The honest limitation statement is importan | unknown / no anchor | [ANCHOR-PROJECT-LIMITATIONS] | unknown / no anchor | partial |  |
| Q20 | Why should this RAG project stop deepening after evaluation, rerank, Qdrant, and metadata filters? | `[ANCHOR-PROJECT-LIMITATIONS]` | `unknown / no anchor` | ed answers. The project is not a generic chatbot. Its main value is that answers should be connected to uploaded source material. The system | unknown / no anchor | [ANCHOR-RETRIEVAL-RANKING] | [ANCHOR-PROJECT-PURPOSE] | fail |  |

## Final Analysis

### Pass Cases

- Q2: top-1 hit [ANCHOR-UPLOAD-PIPELINE]
- Q10: top-1 hit [ANCHOR-PROMPT-BUILDER]
- Q12: top-1 hit [ANCHOR-ANSWER-ENDPOINT]
- Q13: top-1 hit [ANCHOR-CONFIG-ENV]
- Q15: top-1 hit [ANCHOR-RETRIEVAL-EVALUATION]
- Q17: top-1 hit [ANCHOR-QDRANT-PLAN]
- Q18: top-1 hit [ANCHOR-METADATA-FILTER]

### Partial Cases

- Q1: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q3: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q7: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q19: expected anchor appears in top-3, but top-1 is unknown / no anchor

### Fail Cases

- Q4: expected [ANCHOR-STORAGE-LAYER] missing from top-3: [ANCHOR-EMBEDDING-PROVIDER] | unknown / no anchor | [ANCHOR-PROMPT-BUILDER]
- Q5: expected [ANCHOR-EMBEDDING-PROVIDER] missing from top-3: unknown / no anchor | unknown / no anchor | [ANCHOR-PROJECT-PURPOSE]
- Q6: expected [ANCHOR-EMBEDDING-PROVIDER] missing from top-3: unknown / no anchor | unknown / no anchor | unknown / no anchor
- Q8: expected [ANCHOR-RETRIEVAL-RANKING] missing from top-3: unknown / no anchor | unknown / no anchor | [ANCHOR-RERANKING-PLAN]
- Q9: expected [ANCHOR-RETRIEVAL-RANKING] missing from top-3: unknown / no anchor | unknown / no anchor | [ANCHOR-CHUNKING-POLICY]
- Q11: expected [ANCHOR-LLM-CLIENT] missing from top-3: unknown / no anchor | unknown / no anchor | [ANCHOR-PROJECT-PURPOSE]
- Q14: expected [ANCHOR-TESTING-CI] missing from top-3: unknown / no anchor | [ANCHOR-PROMPT-BUILDER] | unknown / no anchor
- Q16: expected [ANCHOR-RERANKING-PLAN] missing from top-3: unknown / no anchor | [ANCHOR-PROJECT-LIMITATIONS] | unknown / no anchor
- Q20: expected [ANCHOR-PROJECT-LIMITATIONS] missing from top-3: unknown / no anchor | [ANCHOR-RETRIEVAL-RANKING] | [ANCHOR-PROJECT-PURPOSE]

### What Rerank Should Improve

- Q1: move expected anchor [ANCHOR-PROJECT-PURPOSE] above current top-1 unknown / no anchor
- Q3: move expected anchor [ANCHOR-CHUNKING-POLICY] above current top-1 unknown / no anchor
- Q7: move expected anchor [ANCHOR-VECTOR-STORE] above current top-1 unknown / no anchor
- Q19: move expected anchor [ANCHOR-PROJECT-LIMITATIONS] above current top-1 unknown / no anchor

### What Retrieval Or Content Should Improve

- Q4: expected anchor [ANCHOR-STORAGE-LAYER] did not appear in top-3
- Q5: expected anchor [ANCHOR-EMBEDDING-PROVIDER] did not appear in top-3
- Q6: expected anchor [ANCHOR-EMBEDDING-PROVIDER] did not appear in top-3
- Q8: expected anchor [ANCHOR-RETRIEVAL-RANKING] did not appear in top-3
- Q9: expected anchor [ANCHOR-RETRIEVAL-RANKING] did not appear in top-3
- Q11: expected anchor [ANCHOR-LLM-CLIENT] did not appear in top-3
- Q14: expected anchor [ANCHOR-TESTING-CI] did not appear in top-3
- Q16: expected anchor [ANCHOR-RERANKING-PLAN] did not appear in top-3
- Q20: expected anchor [ANCHOR-PROJECT-LIMITATIONS] did not appear in top-3

### Next Experiment

- Use this baseline to compare the rerank results. Focus first on partial cases, because the correct evidence is already retrieved but ranked too low.
