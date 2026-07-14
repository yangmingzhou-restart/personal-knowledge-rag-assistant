# Retrieval Evaluation

## Evaluation Goal

Retrieval evaluation checks whether `/retrieve` returns the chunks that actually answer the user question. It is different from checking whether the endpoint runs. A successful endpoint can still return weak evidence.

Current retrieval flow:

1. `/upload` stores document metadata and chunks.
2. The embedding provider embeds each chunk.
3. The vector store stores embeddings.
4. `/retrieve` embeds the user question.
5. The vector store ranks chunks by cosine similarity.
6. The API returns top-k matches with source fields and scores.

## Current Baseline

The current baseline uses:

- sample document: `eval/sample-personal-knowledge.md`
- questions: `eval/evaluation-questions.md`
- output: `eval/evaluation-results.md`
- chunk size: `500`
- overlap: `50`
- top k: `3`

This baseline should be run before changing rerank, Qdrant, metadata filters, or chunking. The goal is to know whether a change improves retrieval quality instead of only changing code structure.

## Status Definitions

A returned chunk can contain multiple anchors because fixed-size chunking may cross markdown section boundaries.

The evaluation script should:

1. extract all anchors from each returned chunk;
2. treat top-1 as pass when the first returned chunk contains the expected anchor;
3. treat top-k as partial when a later returned chunk contains the expected anchor;
4. treat it as fail only when the expected anchor is absent from all returned chunks.

## Failure Types

### 1. Chunk Boundary Failure

Fixed character chunking can cut a markdown section in the middle. A returned chunk may start with text from the previous section and only later contain the section that answers the question.

Symptom:

- evidence looks relevant, but the detected anchor is `unknown / no anchor` or belongs to the previous section.

Likely improvement:

- improve evaluation anchor detection first;
- later consider markdown-aware chunking.

### 2. Embedding Semantic Drift

Embedding retrieval ranks by vector similarity. It may prefer broad project-description chunks when the question contains general words such as `project`, `provider`, `handle`, or `useful`.

Symptom:

- top-1 is a general project-purpose chunk;
- the expected engineering boundary appears lower or outside top-3.

Likely improvement:

- retrieve more candidates;
- add a rerank step.

### 3. Anchor Judgment Error

The evaluation script can misjudge retrieval when it only extracts one anchor from each chunk. If a chunk contains the expected anchor later in the text, the script may still mark it as wrong.

Symptom:

- the chunk text contains the expected evidence;
- the recorded top-1 anchor does not match the expected anchor.

Likely improvement:

- extract all anchors from each returned chunk;
- judge whether the expected anchor appears anywhere in the returned evidence.

### 4. Top-k Too Small

When `top_k=3`, useful chunks may appear at rank 4 or rank 5. This is still valuable diagnostic information, because rerank often works by retrieving a wider candidate set before reordering.

Symptom:

- expected chunk appears in top-5 diagnostics but not in top-3 evaluation.

Likely improvement:

- use top-10 candidates internally;
- rerank candidates;
- return final top-3 to the user.

## Optimization Order

1. Improve evaluation anchor detection.
2. Keep the current results as a baseline.
3. Add rerank with a wider candidate set.
4. Compare rerank results against the baseline.
5. Add Qdrant behind the vector store boundary.
6. Add metadata filters for multi-document retrieval.

## Interview Explanation

The important point is that retrieval quality must be measured separately from API correctness. In this project, `/retrieve` can run correctly while still returning weak evidence. I built a small evaluation set with expected anchors, recorded pass/partial/fail cases, and used the failure pattern to decide the next engineering step. The current evidence suggests rerank and better evaluation logic are more urgent than changing the API endpoint.
