# Metadata Filtering

Current supported filters:

- document_id
- source
- document_type

Limitations:

- no user permission system yet
- no workspace isolation yet
- no complex tag query yet
- Qdrant payload filtering supports the current metadata fields behind the VectorStore boundary.

Example document types should use product or knowledge-base labels such as `note`, `policy`, `resume`, or `faq`, rather than job-search-only labels.
