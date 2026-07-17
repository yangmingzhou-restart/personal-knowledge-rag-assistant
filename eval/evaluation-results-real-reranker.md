# Retrieval Evaluation Results

Date: 2026-07-17T07:43:24.158397+00:00
Sample document: `D:\AI创业\找工作\ai-rag-agent-learning-system\generated\portfolio\personal-knowledge-rag\eval\sample-personal-knowledge.md`
Document ID: doc_984d04125b7f
Chunk size: 500
Overlap: 50
Top k: 3

## Summary

| Metric | Result |
| --- | --- |
| Total questions | 20 |
| Pass | 10 |
| Partial | 6 |
| Fail | 4 |

## Detailed Results

| ID | Question | Expected anchor | Top-1 anchor | Top-1 evidence | Top-3 anchors | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | What is the  main purpose of the Personal Knowledge RAG Assistant? | `[ANCHOR-PROJECT-PURPOSE]` | `[ANCHOR-PROJECT-PURPOSE]` | ual evaluation, use the anchor label and nearby content to judge whether retrieval found the expected evidence. The anchor labels are not me | [ANCHOR-PROJECT-PURPOSE] ; unknown / no anchor ; [ANCHOR-PROJECT-LIMITATIONS] | pass |  |
| Q2 | What happens after a user uploads a file? | `[ANCHOR-UPLOAD-PIPELINE]` | `[ANCHOR-UPLOAD-PIPELINE]` | g, prompt construction, and LLM provider boundaries. The goal is not to build a perfect enterprise system immediately. The goal is to build  | [ANCHOR-UPLOAD-PIPELINE] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q3 | What should the chunking module be responsible for? | `[ANCHOR-CHUNKING-POLICY]` | `[ANCHOR-CHUNKING-POLICY]` | future implementation, the same boundary can write vectors to Qdrant or another vector database. ## Section 03 - Chunking Policy [ANCHOR-CHU | [ANCHOR-CHUNKING-POLICY] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q4 | Why does get_chunks_by_document convert embedding_json back into a list of floats? | `[ANCHOR-STORAGE-LAYER]` | `[ANCHOR-EMBEDDING-PROVIDER]` | and converts embedding_json back into a Python list of floats. This conversion is important because retrieval code expects embeddings as lis | [ANCHOR-EMBEDDING-PROVIDER] ; unknown / no anchor ; unknown / no anchor | fail |  |
| Q5 | Why does the project use an EmbeddingProvider boundary? | `[ANCHOR-EMBEDDING-PROVIDER]` | `unknown / no anchor` | MBEDDING-PROVIDER] The embedding provider boundary hides the details of converting text into vectors. The same upload and retrieval flows sh | unknown / no anchor ; [ANCHOR-EMBEDDING-PROVIDER] ; unknown / no anchor | partial |  |
| Q6 | Why should the local BGE embedding model not be loaded on every request? | `[ANCHOR-EMBEDDING-PROVIDER]` | `unknown / no anchor` | t does not represent real semantic similarity, but it makes tests stable and fast. LocalEmbeddingProvider uses a sentence-transformers model | unknown / no anchor ; [ANCHOR-TESTING-CI] ; unknown / no anchor | fail |  |
| Q7 | Why should main.py use get_vector_store instead of directly importing SQLiteVectorStore? | `[ANCHOR-VECTOR-STORE]` | `unknown / no anchor` | ging the API endpoint shape. The API should ask for a vector store through get_vector_store rather than directly importing a concrete implem | unknown / no anchor ; [ANCHOR-VECTOR-STORE] ; unknown / no anchor | partial |  |
| Q8 | How are chunks ranked during retrieval? | `[ANCHOR-RETRIEVAL-RANKING]` | `unknown / no anchor` | # Personal Knowledge RAG Evaluation Sample This document is intentionally longer than a normal quick demo note. With the current chunking se | unknown / no anchor ; unknown / no anchor ; [ANCHOR-RERANKING-PLAN] | fail |  |
| Q9 | Why does one chunk have one embedding vector instead of one vector per character? | `[ANCHOR-RETRIEVAL-RANKING]` | `unknown / no anchor` | ss embeds the user question and compares the query embedding with stored chunk embeddings. The ranking function uses cosine similarity. A hi | unknown / no anchor ; unknown / no anchor ; unknown / no anchor | fail |  |
| Q10 | What does the grounded prompt builder do? | `[ANCHOR-PROMPT-BUILDER]` | `[ANCHOR-PROMPT-BUILDER]` | That may require better chunking, better documents, better embeddings, metadata filters, or query rewriting. ## Section 08 - Grounded Prompt | [ANCHOR-PROMPT-BUILDER] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q11 | How should the project handle an Ollama provider failure? | `[ANCHOR-LLM-CLIENT]` | `unknown / no anchor` | er is fake or real. It should only call a common generate method. The Ollama client sends a POST request to the local Ollama API. It uses a  | unknown / no anchor ; [ANCHOR-LLM-CLIENT] ; [ANCHOR-TESTING-CI] | partial |  |
| Q12 | What should the answer endpoint return besides the final answer? | `[ANCHOR-ANSWER-ENDPOINT]` | `unknown / no anchor` | ent and returns an answer, provider name, sources, and confidence notes. The answer endpoint should not duplicate retrieval logic. If retrie | unknown / no anchor ; [ANCHOR-ANSWER-ENDPOINT] ; unknown / no anchor | partial |  |
| Q13 | What is the relationship between .env, config.py, and settings? | `[ANCHOR-CONFIG-ENV]` | `[ANCHOR-CONFIG-ENV]` | ibility is central to a RAG application. Without sources, the user cannot easily inspect whether the model answer is actually grounded. ## S | [ANCHOR-CONFIG-ENV] ; unknown / no anchor ; [ANCHOR-TESTING-CI] | pass |  |
| Q14 | Why should CI use fake providers by default? | `[ANCHOR-TESTING-CI]` | `[ANCHOR-TESTING-CI]` | names but should not contain private secrets. It is a template for other developers, not the real local configuration file. ## Section 12 -  | [ANCHOR-TESTING-CI] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q15 | How should retrieval evaluation classify pass, partial, and fail? | `[ANCHOR-RETRIEVAL-EVALUATION]` | `unknown / no anchor` | tus can be pass, partial, or fail. Pass means the best returned chunk directly contains the expected evidence. Partial means the expected ev | unknown / no anchor ; [ANCHOR-RETRIEVAL-EVALUATION] ; unknown / no anchor | partial |  |
| Q16 | When is reranking most useful in this project? | `[ANCHOR-RERANKING-PLAN]` | `[ANCHOR-RERANKING-PLAN]` | ch parts of the RAG system work and which parts need improvement. ## Section 14 - Reranking Plan [ANCHOR-RERANKING-PLAN] Reranking is planne | [ANCHOR-RERANKING-PLAN] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q17 | What is the intended first step for adding Qdrant? | `[ANCHOR-QDRANT-PLAN]` | `[ANCHOR-QDRANT-PLAN]` | r measurable benefit. ## Section 15 - Qdrant Plan [ANCHOR-QDRANT-PLAN] Qdrant is a vector database that can store vectors and perform simila | [ANCHOR-QDRANT-PLAN] ; unknown / no anchor ; [ANCHOR-CHUNKING-POLICY] | pass |  |
| Q18 | Why is metadata filtering needed beyond document_id retrieval? | `[ANCHOR-METADATA-FILTER]` | `[ANCHOR-METADATA-FILTER]` | an [ANCHOR-METADATA-FILTER] Single document_id retrieval is useful for learning, but it is limited. Real knowledge bases often search across | [ANCHOR-METADATA-FILTER] ; [ANCHOR-RETRIEVAL-RANKING] ; [ANCHOR-PROJECT-LIMITATIONS] | pass |  |
| Q19 | What limitations should be honestly stated about the current project? | `[ANCHOR-PROJECT-LIMITATIONS]` | `[ANCHOR-PROJECT-LIMITATIONS]` | l is to show how retrieval can move from one-document search toward knowledge-base search. Metadata filters help answer questions such as: s | [ANCHOR-PROJECT-LIMITATIONS] ; unknown / no anchor ; unknown / no anchor | pass |  |
| Q20 | Why should this RAG project stop deepening after evaluation, rerank, Qdrant, and metadata filters? | `[ANCHOR-PROJECT-LIMITATIONS]` | `[ANCHOR-METADATA-FILTER]` | se one collection, upsert vectors for chunks, and search vectors by query embedding. It should not attempt production deployment, advanced r | [ANCHOR-METADATA-FILTER] ; [ANCHOR-PROJECT-LIMITATIONS] ; [ANCHOR-RETRIEVAL-RANKING] | partial |  |

## Final Analysis

### Pass Cases

- Q1: top-1 hit [ANCHOR-PROJECT-PURPOSE]
- Q2: top-1 hit [ANCHOR-UPLOAD-PIPELINE]
- Q3: top-1 hit [ANCHOR-CHUNKING-POLICY]
- Q10: top-1 hit [ANCHOR-PROMPT-BUILDER]
- Q13: top-1 hit [ANCHOR-CONFIG-ENV]
- Q14: top-1 hit [ANCHOR-TESTING-CI]
- Q16: top-1 hit [ANCHOR-RERANKING-PLAN]
- Q17: top-1 hit [ANCHOR-QDRANT-PLAN]
- Q18: top-1 hit [ANCHOR-METADATA-FILTER]
- Q19: top-1 hit [ANCHOR-PROJECT-LIMITATIONS]

### Partial Cases

- Q5: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q7: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q11: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q12: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q15: expected anchor appears in top-3, but top-1 is unknown / no anchor
- Q20: expected anchor appears in top-3, but top-1 is [ANCHOR-METADATA-FILTER]

### Fail Cases

- Q4: expected [ANCHOR-STORAGE-LAYER] missing from top-3: [ANCHOR-EMBEDDING-PROVIDER] ; unknown / no anchor ; unknown / no anchor
- Q6: expected [ANCHOR-EMBEDDING-PROVIDER] missing from top-3: unknown / no anchor ; [ANCHOR-TESTING-CI] ; unknown / no anchor
- Q8: expected [ANCHOR-RETRIEVAL-RANKING] missing from top-3: unknown / no anchor ; unknown / no anchor ; [ANCHOR-RERANKING-PLAN]
- Q9: expected [ANCHOR-RETRIEVAL-RANKING] missing from top-3: unknown / no anchor ; unknown / no anchor ; unknown / no anchor

### What Rerank Should Improve

- Q5: move expected anchor [ANCHOR-EMBEDDING-PROVIDER] above current top-1 unknown / no anchor
- Q7: move expected anchor [ANCHOR-VECTOR-STORE] above current top-1 unknown / no anchor
- Q11: move expected anchor [ANCHOR-LLM-CLIENT] above current top-1 unknown / no anchor
- Q12: move expected anchor [ANCHOR-ANSWER-ENDPOINT] above current top-1 unknown / no anchor
- Q15: move expected anchor [ANCHOR-RETRIEVAL-EVALUATION] above current top-1 unknown / no anchor
- Q20: move expected anchor [ANCHOR-PROJECT-LIMITATIONS] above current top-1 [ANCHOR-METADATA-FILTER]

### What Retrieval Or Content Should Improve

- Q4: expected anchor [ANCHOR-STORAGE-LAYER] did not appear in top-3
- Q6: expected anchor [ANCHOR-EMBEDDING-PROVIDER] did not appear in top-3
- Q8: expected anchor [ANCHOR-RETRIEVAL-RANKING] did not appear in top-3
- Q9: expected anchor [ANCHOR-RETRIEVAL-RANKING] did not appear in top-3

### Next Experiment

- This is rerank results. Focus first on partial cases, because the correct evidence is already retrieved but ranked too low.
| Hit Rate@K | 80.00% |
| Recall@K | 80.00% |
| MRR | 0.6500 |
