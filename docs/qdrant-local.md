# Qdrant Local Integration

## Start Qdrant

```powershell
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

## Use Qdrant Manually

Set `VECTOR_STORE_PROVIDER=qdrant` in `.env`, then start the API and upload a sample document.

## CI Rule

Ordinary pytest and GitHub Actions should keep `VECTOR_STORE_PROVIDER=sqlite`.

Qdrant is an optional local vector store implementation for experiments. The default portfolio demo remains SQLite so tests and CI do not depend on a running Qdrant service.
