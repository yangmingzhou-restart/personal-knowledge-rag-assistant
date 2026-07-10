# RAG Evaluation

This document describes a small manual evaluation set for the Personal Knowledge RAG Assistant.

## Purpose

The goal is to check whether the system retrieves relevant context and generates answers grounded in that context.

## Evaluation files

- 'eval/sample-personal-knowledge.md': sample document used as the knowledge base.
- 'eval/evaluation-questions.md': fixed questions with sources and expoectefd answer points.

## Manual evaluation flow

1. Start the API service.
2. Uplaod 'eval/sample-personal-knowledge.md' throught '/upload/'
3. Copy the returned 'document_id'
4. For each question in 'eval/evaluation-questions.md', call '/retrieve' first.
5. Check whether returned matches contain the expoecrted source section.
6. Call '/answer' with the same question.
7. Check whether the answer uses the retrieved context and includes source information.

## What to evaluate

| Criterion | Good result | Weak result |
|---|---|---|
| Retrieval relevance | Top matches contain the expected section | Top matches are unrelated |
| Grounding | Answer is based on retrieved context | Answer uses outside knowledge |
| Source traceability | Response includes useful sources | Response has no source references |
| Insufficient context handling | Says context is insufficient | Hallucinates an answer |
| Safety | Provider failures return controlled errors | Raw provider errors leak to users |

## Current limitations

The project still uses fake embeddings and a fake LLM client, so this evaluation mainly verifies pipeline behavior, source tracking, and failure handling. It does not yet prove production-grade semantic retrieval quality. 

