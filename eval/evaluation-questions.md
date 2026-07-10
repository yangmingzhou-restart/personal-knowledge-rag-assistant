# RAG Evaluation Questions

## How to read this file

- `Question`: the user question.
- `Expected source section`: the section that should be retrieved.
- `Expected answer points`: facts that should appear in a grounded answer.
- `Failure signal`: what would indicate a weak RAG answer.

## Questions

### 1. What is the goal of this assistant?

- Expected source section: Project Goal
- Expected answer points:
  - upload notes
  - split notes into chunks
  - retrieve relevant context
  - generate grounded answers
- Failure signal: answer talks about general chatbots but not uploaded notes or grounded answers

### 2. What does the upload endpoint do?

- Expected source section: Architecture
- Expected answer points:
  - extracts text
  - chunks text
  - stores metadata in SQLite
  - writes fake embeddings
- Failure signal: answer only says "uploads files" without pipeline details

### 3. What inputs does the retrieval endpoint receive?

- Expected source section: Retrieval
- Expected answer points:
  - document_id
  - question
  - top_k
- Failure signal: missing top_k or document_id

### 4. How are chunks ranked?

- Expected source section: Retrieval
- Expected answer points:
  - question embedding
  - stored chunk embeddings
  - cosine similarity
  - top matches
- Failure signal: says keyword search or database order only

### 5. What does the answer endpoint return besides the answer?

- Expected source section: Generation
- Expected answer points:
  - sources
  - grounded answer
  - answer from LLM client
- Failure signal: ignores sources

### 6. What should happen when the LLM provider fails?

- Expected source section: Safety
- Expected answer points:
  - controlled 503 response
  - no provider internals exposed
- Failure signal: answer exposes raw error details

### 7. Why are fake embeddings used?

- Expected source section: Limitations
- Expected answer points:
  - stable tests
  - local development
  - not real semantic quality
- Failure signal: claims fake embeddings are production-grade

### 8. What is a limitation of the current project?

- Expected source section: Limitations
- Expected answer points:
  - fake embeddings
  - fake LLM client
  - does not measure real semantic retrieval quality
- Failure signal: says there are no limitations