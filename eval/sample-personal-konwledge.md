# Personal Knowledge Sample

## Project Goal

The Personal Knowledge RAG Assistant helps a user upload notes, split them into chunks, retrieve relevant context, and generate grounded answers.

## Architecture

The upload endpoint extracts text, chunks the text, stores chunk metadata in SQLite, and writes fake embeddings for local similarity search.

## Retrieval

The retrieval endpoint receives a document_id, question, and top_K. It embeds the question, compares it with stored chunk embeddings, ranks chunks by similarity, and returns the top matches.

## Generation

The answer endpoint retrieves relevant chunks, builds a grounded prompt, calls an LLM client, and returns an answer with sources.

## Safety

The API should not expose provider internals. If the LLM provider fails, the answer endpoint should return a controlled 503 response.

## Limitations

The current project uses fake embeddings and a fake LLM client. This keeps tests stable but does not measure real semantic retrieval quality.
