# RAG Evaluation

This document describes a small anchor-based evaluation set for the Personal Knowledge RAG Assistant. It can run through the reranker stage and report Hit Rate@K, Recall@K, and MRR.

## Purpose

The goal is to check whether the system retrieves relevant context and generates answers grounded in that context.

## Evaluation files

- `eval/sample-personal-knowledge.md`: sample document used as the knowledge base.
- `eval/evaluation-questions.md`: fixed questions with sources and expected answer points.

## Evaluation flow

1. Start the API service.
2. Upload `eval/sample-personal-knowledge.md` through `/upload`.
3. Copy the returned `document_id`.
4. For each question in `eval/evaluation-questions.md`, call `/retrieve` first.
5. Check whether returned matches contain the expected source section.
6. Call `/answer` with the same question.
7. Check whether the answer uses the retrieved context and includes source information.

## What to evaluate

| Criterion | Good result | Weak result |
|---|---|---|
| Retrieval relevance | Top matches contain the expected section | Top matches are unrelated |
| Grounding | Answer is based on retrieved context | Answer uses outside knowledge |
| Source traceability | Response includes useful sources | Response has no source references |
| Insufficient context handling | Says context is insufficient | Hallucinates an answer |
| Safety | Provider failures return controlled errors | Raw provider errors leak to users |

## Current status

The project supports local BGE embeddings, reranker-based retrieval evaluation, and local Ollama answer generation. This evaluation focuses on whether retrieval and reranking return useful evidence before the final answer is generated.
