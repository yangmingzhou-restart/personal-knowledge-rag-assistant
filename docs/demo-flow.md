# Demo Flow

## 1. Start Server

```powershell
C:\Users\YangMingZhou\anaconda3\python.exe -m uvicorn app.main:app --reload
```

Open: 

```text
http://127.0.0.1:8000/docs
```

## 2. Health Check

Call:

```text
GET /health
```

Expected:

```json
{"status": "ok"}
```

## 3. Upload

Call:

```text
POST /upload
```

Upload `hello.txt`:

```text
RAG uses retrieved context.
```

Copy returned `document_id`.

## 4. Retrieve

Call:

```text
POST /retrieve
```

Body:

```json
{
    "document_id": "doc_xxx",
    "question": "What does RAG use?",
    "top_k": 3
}
```

## 5. Answer

Call:

```text
POST /answer
```

Body:

```json
{
    "document_id": "doc_xxx",
    "question": "What does RAG use?",
    "top_k": 3
}
```

Check `answer`, `sources`, and `confidence_notes`.
