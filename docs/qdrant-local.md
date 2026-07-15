# Qdrant Local Integration

## Start Qdrant

```powershell
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

## User Qdrant Manually

Set `VECTOR_STORE_PROVIDER=qdrant` in `.env`, then start the API and upload a sample document.

## CI Rule

Ordinary pytest and Github Actions should keep `VECTOR_STORE_PROVIDER=sqlite`.
