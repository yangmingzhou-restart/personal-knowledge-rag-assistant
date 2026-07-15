# Retrieval Evaluation Results

Date: 2026-07-14T08:07:15.233993+00:00
Sample document: `D:\AI创业\找工作\ai-rag-agent-learning-system\generated\portfolio\personal-knowledge-rag\eval\sample-personal-knowledge.md`
Document ID: doc_bc0f5822ba15
Chunk size: 500
Overlap: 50
Top k: 3

## Summary

| Metric | Result |
| --- | --- |
| Total questions | 20 |
| Pass | 11 |
| Partial | 4 |
| Fail | 5 |

## Detailed Results

| ID | Question | Expected anchor | Top-1 anchor | Top-1 evidence | Top-3 anchors | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | What is the  main purpose of the Personal Knowledge RAG Assistant? | `[ANCHOR-PROJECT-PURPOSE]` | `unknown / no anchor` | # Personal Knowledge RAG Evaluation Sample This document is intentionally longer than a normal quick demo note. With the current chunking se | unknown / no anchor ; [ANCHOR-PROJECT-PURPOSE] ; unknown / no anchor | partial |  |
| Q2 | What happens after a user uploads a file? | `[ANCHOR-UPLOAD-PIPELINE]` | `[ANCHOR-PROMPT-BUILDER]` | That may require better chunking, better documents, better embeddings, metadata filters, or query rewriting. ## Section 08 - Grounded Prompt | [ANCHOR-PROMPT-BUILDER] ; unknown / no anchor ; unknown / no anchor | fail |  |
| Q3 | What should the chunking module be responsible for? | `[ANCHOR-CHUNKING-POLICY]` | `[ANCHOR-CHUNKING-POLICY]` | future implementation, the same boundary can write vectors to Qdrant or another vector database. ## Section 03 - Chunking Policy [ANCHOR-CHU | [ANCHOR-CHUNKING-POLICY] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q4 | Why does get_chunks_by_document convert embedding_json back into a list of floats? | `[ANCHOR-STORAGE-LAYER]` | `[ANCHOR-EMBEDDING-PROVIDER]` | and converts embedding_json back into a Python list of floats. This conversion is important because retrieval code expects embeddings as lis | [ANCHOR-EMBEDDING-PROVIDER] ; unknown / no anchor ; unknown / no anchor | fail |  |
| Q5 | Why does the project use an EmbeddingProvider boundary? | `[ANCHOR-EMBEDDING-PROVIDER]` | `[ANCHOR-LLM-CLIENT]` | hes that were already retrieved. This keeps retrieval, prompt construction, and LLM generation as separate responsibilities. ## Section 09 - | [ANCHOR-LLM-CLIENT] ; unknown / no anchor ; [ANCHOR-PROJECT-PURPOSE] | fail |  |
| Q6 | Why should the local BGE embedding model not be loaded on every request? | `[ANCHOR-EMBEDDING-PROVIDER]` | `unknown / no anchor` | t does not represent real semantic similarity, but it makes tests stable and fast. LocalEmbeddingProvider uses a sentence-transformers model | unknown / no anchor ; [ANCHOR-TESTING-CI] ; [ANCHOR-EMBEDDING-PROVIDER] | partial |  |
| Q7 | Why should main.py use get_vector_store instead of directly importing SQLiteVectorStore? | `[ANCHOR-VECTOR-STORE]` | `unknown / no anchor` | ging the API endpoint shape. The API should ask for a vector store through get_vector_store rather than directly importing a concrete implem | unknown / no anchor ; [ANCHOR-METADATA-FILTER] ; [ANCHOR-VECTOR-STORE] | partial |  |
| Q8 | How are chunks ranked during retrieval? | `[ANCHOR-RETRIEVAL-RANKING]` | `unknown / no anchor` | , and end_char. These fields are important because later retrieval results need to point back to the original source position. The upload en | unknown / no anchor ; unknown / no anchor ; unknown / no anchor | fail |  |
| Q9 | Why does one chunk have one embedding vector instead of one vector per character? | `[ANCHOR-RETRIEVAL-RANKING]` | `unknown / no anchor` | ss embeds the user question and compares the query embedding with stored chunk embeddings. The ranking function uses cosine similarity. A hi | unknown / no anchor ; unknown / no anchor ; [ANCHOR-RERANKING-PLAN] | fail |  |
| Q10 | What does the grounded prompt builder do? | `[ANCHOR-PROMPT-BUILDER]` | `[ANCHOR-PROMPT-BUILDER]` | That may require better chunking, better documents, better embeddings, metadata filters, or query rewriting. ## Section 08 - Grounded Prompt | [ANCHOR-PROMPT-BUILDER] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q11 | How should the project handle an Ollama provider failure? | `[ANCHOR-LLM-CLIENT]` | `[ANCHOR-LLM-CLIENT]` | hes that were already retrieved. This keeps retrieval, prompt construction, and LLM generation as separate responsibilities. ## Section 09 - | [ANCHOR-LLM-CLIENT] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q12 | What should the answer endpoint return besides the final answer? | `[ANCHOR-ANSWER-ENDPOINT]` | `[ANCHOR-ANSWER-ENDPOINT]` | not leak private details or raw stack traces to the user. A stable API should return a clear error message and status code while keeping int | [ANCHOR-ANSWER-ENDPOINT] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q13 | What is the relationship between .env, config.py, and settings? | `[ANCHOR-CONFIG-ENV]` | `[ANCHOR-CONFIG-ENV]` | ibility is central to a RAG application. Without sources, the user cannot easily inspect whether the model answer is actually grounded. ## S | [ANCHOR-CONFIG-ENV] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q14 | Why should CI use fake providers by default? | `[ANCHOR-TESTING-CI]` | `[ANCHOR-TESTING-CI]` | names but should not contain private secrets. It is a template for other developers, not the real local configuration file. ## Section 12 -  | [ANCHOR-TESTING-CI] ; [ANCHOR-LLM-CLIENT] ; unknown / no anchor | pass |  |
| Q15 | How should retrieval evaluation classify pass, partial, and fail? | `[ANCHOR-RETRIEVAL-EVALUATION]` | `[ANCHOR-RETRIEVAL-EVALUATION]` | l evaluation can record real retrieval quality in markdown files, while CI checks basic structure and core deterministic behavior. ## Sectio | [ANCHOR-RETRIEVAL-EVALUATION] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q16 | When is reranking most useful in this project? | `[ANCHOR-RERANKING-PLAN]` | `[ANCHOR-RERANKING-PLAN]` | ch parts of the RAG system work and which parts need improvement. ## Section 14 - Reranking Plan [ANCHOR-RERANKING-PLAN] Reranking is planne | [ANCHOR-RERANKING-PLAN] ; [ANCHOR-PROJECT-LIMITATIONS] ; unknown / no anchor | pass |  |
| Q17 | What is the intended first step for adding Qdrant? | `[ANCHOR-QDRANT-PLAN]` | `[ANCHOR-QDRANT-PLAN]` | r measurable benefit. ## Section 15 - Qdrant Plan [ANCHOR-QDRANT-PLAN] Qdrant is a vector database that can store vectors and perform simila | [ANCHOR-QDRANT-PLAN] ; unknown / no anchor ; [ANCHOR-RERANKING-PLAN] | pass |  |
| Q18 | Why is metadata filtering needed beyond document_id retrieval? | `[ANCHOR-METADATA-FILTER]` | `[ANCHOR-METADATA-FILTER]` | an [ANCHOR-METADATA-FILTER] Single document_id retrieval is useful for learning, but it is limited. Real knowledge bases often search across | [ANCHOR-METADATA-FILTER] ; [ANCHOR-METADATA-FILTER] ; [ANCHOR-RETRIEVAL-RANKING] | pass |  |
| Q19 | What limitations should be honestly stated about the current project? | `[ANCHOR-PROJECT-LIMITATIONS]` | `[ANCHOR-PROJECT-LIMITATIONS]` | l is to show how retrieval can move from one-document search toward knowledge-base search. Metadata filters help answer questions such as: s | [ANCHOR-PROJECT-LIMITATIONS] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q20 | Why should this RAG project stop deepening after evaluation, rerank, Qdrant, and metadata filters? | `[ANCHOR-PROJECT-LIMITATIONS]` | `unknown / no anchor` | ent and returns an answer, provider name, sources, and confidence notes. The answer endpoint should not duplicate retrieval logic. If retrie | unknown / no anchor ; [ANCHOR-PROJECT-LIMITATIONS] ; [ANCHOR-METADATA-FILTER] | partial |  |

## Final Analysis

### Pass Cases

- Q3: top-1 hit [ANCHOR-CHUNKING-POLICY]
- Q10: top-1 hit [ANCHOR-PROMPT-BUILDER]
- Q11: top-1 hit [ANCHOR-LLM-CLIENT]
- Q12: top-1 hit [ANCHOR-ANSWER-ENDPOINT]
- Q13: top-1 hit [ANCHOR-CONFIG-ENV]
- Q14: top-1 hit [ANCHOR-TESTING-CI]
- Q15: top-1 hit [ANCHOR-RETRIEVAL-EVALUATION]
- Q16: top-1 hit [ANCHOR-RERANKING-PLAN]
- Q17: top-1 hit [ANCHOR-QDRANT-PLAN]
- Q18: top-1 hit [ANCHOR-METADATA-FILTER]
- Q19: top-1 hit [ANCHOR-PROJECT-LIMITATIONS]

### Partial Cases

- Q1: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q6: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q7: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q20: expected anchor appears in top-3, but top-1 is unknown / no anchor

### Fail Cases

- Q2: expected [ANCHOR-UPLOAD-PIPELINE] missing from top-3: [ANCHOR-PROMPT-BUILDER] ; unknown / no anchor ; unknown / no anchor
- Q4: expected [ANCHOR-STORAGE-LAYER] missing from top-3: [ANCHOR-EMBEDDING-PROVIDER] ; unknown / no anchor ; unknown / no anchor
- Q5: expected [ANCHOR-EMBEDDING-PROVIDER] missing from top-3: [ANCHOR-LLM-CLIENT] ; unknown / no anchor ; [ANCHOR-PROJECT-PURPOSE]
- Q8: expected [ANCHOR-RETRIEVAL-RANKING] missing from top-3: unknown / no anchor ; unknown / no anchor ; unknown / no anchor
- Q9: expected [ANCHOR-RETRIEVAL-RANKING] missing from top-3: unknown / no anchor ; unknown / no anchor ; [ANCHOR-RERANKING-PLAN]

### What Rerank Should Improve

- Q1: move expected anchor [ANCHOR-PROJECT-PURPOSE] above current top-1 unknown / no anchor
- Q6: move expected anchor [ANCHOR-EMBEDDING-PROVIDER] above current top-1 unknown / no anchor
- Q7: move expected anchor [ANCHOR-VECTOR-STORE] above current top-1 unknown / no anchor
- Q20: move expected anchor [ANCHOR-PROJECT-LIMITATIONS] above current top-1 unknown / no anchor

### What Retrieval Or Content Should Improve

- Q2: expected anchor [ANCHOR-UPLOAD-PIPELINE] did not appear in top-3
- Q4: expected anchor [ANCHOR-STORAGE-LAYER] did not appear in top-3
- Q5: expected anchor [ANCHOR-EMBEDDING-PROVIDER] did not appear in top-3
- Q8: expected anchor [ANCHOR-RETRIEVAL-RANKING] did not appear in top-3
- Q9: expected anchor [ANCHOR-RETRIEVAL-RANKING] did not appear in top-3

### Next Experiment

- Use this baseline to compare the rerank results. Focus first on partial cases, because the correct evidence is already retrieved but ranked too low.
