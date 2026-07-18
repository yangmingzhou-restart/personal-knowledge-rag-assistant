# RAG Evaluation Questions

## How to use this file

Use this file before changing rerank, Qdrant, or metadata filters. Upload `eval/sample-personal-konwledge.md`, call `/retrieve` with `top_k=3`, and compare the returned chunks against the expected anchor.

This sample document is intentionally long enough to create many chunks with the current chunk settings. Therefore `top_k=3` should not return the whole document.

For each question, record the actual result in `eval/evaluation-results.md`.

## Question format

- `Question`: the user question sent to `/retrieve`.
- `Expected anchor`: the unique label that should appear in the retrieved evidence.
- `Expected evidence`: the ideas that should appear in a good retrieved chunk.
- `Question type`: the evaluation category.
- `Failure signal`: what suggests retrieval missed the target.

## Questions

### Q1 - Project purpose

- Question: What is the  main purpose of the Personal Knowledge RAG Assistant?
- Expected anchor: `[ANCHOR-PROJECT-PURPOSE]`
- Expected evidence:
  - upload personal notes
  - split notes into chunks
  - retrieve relevant context
  - generate grounded answers connected to source material
- Question type: definition
- Failure signal: retrieved chunks talk about generic chatbots, Qdrant, or testing instead of the project goal

### Q2 - Upload pipeline

- Question: What happens after a user uploads a file?
- Expected anchor: `[ANCHOR-UPLOAD-PIPELINE]`
- Expected evidence:
  - reject empty files
  - extract text
  - store document metadata
  - split text into chunks
  - create and persist embeddings
- Question type: pipeline
- Failure signal: retrieved chunks only say files are uploaded without explaining extraction, chunking, storage, or embeddings

### Q3 - Chunking responsibility

- Question: What should the chunking module be responsible for?
- Expected anchor: `[ANCHOR-CHUNKING-POLICY]`
- Expected evidence:
  - split text into chunks
  - attach source character ranges
  - not call embedding models
  - not decide HTTP status codes
- Question type: implementation boundary
- Failure signal: retrieved chunks describe vector search, LLM calls, or provider config instead of chunking responsibility

### Q4 - Storage layer

- Question: Why does get_chunks_by_document convert embedding_json back into a list of floats?
- Expected anchor: `[ANCHOR-STORAGE-LAYER]`
- Expected evidence:
  - embedding_json is serialized storage format
  - retrieval expects list[float]
  - storage owns persistence and data shape
- Question type: implementation detail
- Failure signal: retrieved chunks discuss prompt building or LLM provider errors instead of storage conversion

### Q5 - Embedding provider boundary

- Question: Why does the project use an EmbeddingProvider boundary?
- Expected anchor: `[ANCHOR-EMBEDDING-PROVIDER]`
- Expected evidence:
  - hide fake/local/future API embedding details
  - expose embed_text and embed_chunks
  - support fake provider for tests and local provider for real retrieval
- Question type: architecture boundary
- Failure signal: retrieved chunks only explain cosine similarity or Qdrant without provider abstraction

### Q6 - Model cache

- Question: Why should the local BGE embedding model not be loaded on every request?
- Expected anchor: `[ANCHOR-EMBEDDING-PROVIDER]`
- Expected evidence:
  - loading model files is expensive
  - tokenizer and neural weights take time and memory
  - provider cache can reuse one loaded provider
  - tests need a reset function
- Question type: performance
- Failure signal: retrieved chunks do not mention repeated model loading, memory, or provider cache

### Q7 - Vector store boundary

- Question: Why should main.py use get_vector_store instead of directly importing SQLiteVectorStore?
- Expected anchor: `[ANCHOR-VECTOR-STORE]`
- Expected evidence:
  - hide concrete vector store implementation
  - current implementation is SQLite
  - future implementation can be Qdrant
  - API endpoint shape does not need to change
- Question type: architecture boundary
- Failure signal: retrieved chunks talk only about upload pipeline or LLM client instead of vector store abstraction

### Q8 - Retrieval ranking

- Question: How are chunks ranked during retrieval?
- Expected anchor: `[ANCHOR-RETRIEVAL-RANKING]`
- Expected evidence:
  - embed the user question
  - compare query embedding with chunk embeddings
  - use cosine similarity
  - return highest scoring chunks first
- Question type: retrieval
- Failure signal: retrieved chunks claim keyword search, database order, or LLM generation performs ranking

### Q9 - Chunk embedding shape

- Question: Why does one chunk have one embedding vector instead of one vector per character?
- Expected anchor: `[ANCHOR-RETRIEVAL-RANKING]`
- Expected evidence:
  - embedding represents the whole chunk
  - model tokenizes text
  - transformer and pooling create one chunk-level vector
  - BGE output can be a fixed-size vector such as 512 dimensions
- Question type: embedding concept
- Failure signal: retrieved chunks do not mention pooling, whole chunk representation, or fixed-size vector

### Q10 - Grounded prompt builder

- Question: What does the grounded prompt builder do?
- Expected anchor: `[ANCHOR-PROMPT-BUILDER]`
- Expected evidence:
  - convert retrieved chunks into context
  - separate source context from user question
  - instruct model to answer only from context
  - preserve source information
- Question type: prompt design
- Failure signal: retrieved chunks discuss chunk storage or Qdrant but not source-grounded prompt construction

### Q11 - LLM client errors

- Question: How should the project handle an Ollama provider failure?
- Expected anchor: `[ANCHOR-LLM-CLIENT]`
- Expected evidence:
  - raise LLMProviderError
  - API converts provider error into controlled response
  - avoid leaking raw stack traces or provider internals
- Question type: error handling
- Failure signal: retrieved chunks recommend exposing raw provider details or ignore error handling

### Q12 - Answer endpoint

- Question: What should the answer endpoint return besides the final answer?
- Expected anchor: `[ANCHOR-ANSWER-ENDPOINT]`
- Expected evidence:
  - provider name
  - sources
  - confidence notes
  - answer grounded in retrieved chunks
- Question type: API response
- Failure signal: retrieved chunks only discuss retrieval ranking and do not mention sources

### Q13 - Configuration

- Question: What is the relationship between .env, config.py, and settings?
- Expected anchor: `[ANCHOR-CONFIG-ENV]`
- Expected evidence:
  - .env provides concrete local values
  - config.py reads values into Settings
  - modules import shared settings
  - tests often patch settings directly
- Question type: configuration
- Failure signal: retrieved chunks say every module should read environment variables directly

### Q14 - Testing and CI

- Question: Why should CI use fake providers by default?
- Expected anchor: `[ANCHOR-TESTING-CI]`
- Expected evidence:
  - avoid local BGE model dependency
  - avoid running Ollama service
  - avoid local Qdrant container dependency
  - keep tests reproducible
- Question type: testing
- Failure signal: retrieved chunks require real local models or services for ordinary CI

### Q15 - Retrieval evaluation

- Question: How should retrieval evaluation classify pass, partial, and fail?
- Expected anchor: `[ANCHOR-RETRIEVAL-EVALUATION]`
- Expected evidence:
  - pass means top-1 directly contains expected evidence
  - partial means top-3 contains expected evidence but top-1 is not best or evidence is incomplete
  - fail means top-3 misses expected evidence
- Question type: evaluation
- Failure signal: retrieved chunks do not distinguish top-1 and top-3

### Q16 - Reranking plan

- Question: When is reranking most useful in this project?
- Expected anchor: `[ANCHOR-RERANKING-PLAN]`
- Expected evidence:
  - vector store retrieves more candidates
  - reranker reorders candidates
  - useful when correct chunk appears in top-3 or top-10 but not rank one
  - should be judged against baseline
- Question type: rerank
- Failure signal: retrieved chunks claim reranking replaces evaluation or vector search entirely

### Q17 - Qdrant plan

- Question: What is the intended first step for adding Qdrant?
- Expected anchor: `[ANCHOR-QDRANT-PLAN]`
- Expected evidence:
  - run Qdrant locally through Docker
  - add QdrantVectorStore behind VectorStore boundary
  - keep SQLite as default provider for tests and CI
  - keep first integration small
- Question type: vector database
- Failure signal: retrieved chunks describe full production deployment or Qdrant Cloud as the first required step

### Q18 - Metadata filters

- Question: Why is metadata filtering needed beyond document_id retrieval?
- Expected anchor: `[ANCHOR-METADATA-FILTER]`
- Expected evidence:
  - real knowledge bases search across many documents
  - filters can use source, document_type, tags, workspace, user, or created_at
  - project will add a small metadata filter step
- Question type: realistic retrieval
- Failure signal: retrieved chunks say document_id-only retrieval is enough for all company use cases

### Q19 - Project limitations

- Question: What limitations should be honestly stated about the current project?
- Expected anchor: `[ANCHOR-PROJECT-LIMITATIONS]`
- Expected evidence:
  - not a production enterprise platform
  - no full authentication
  - no user-level permissions
  - no production monitoring
  - no large-scale ingestion queues
- Question type: limitation
- Failure signal: retrieved chunks claim the project is already production enterprise ready

### Q20 - RAG learning scope

- Question: Why should this RAG project stop deepening after evaluation, rerank, Qdrant, and metadata filters?
- Expected anchor: `[ANCHOR-PROJECT-LIMITATIONS]`
- Expected evidence:
  - project focuses on practical AI application engineering
  - does not solve every production concern
  - honest scope control matters
- Question type: learning strategy
- Failure signal: retrieved chunks suggest endless RAG infrastructure expansion without moving to Agent or SFT learning
