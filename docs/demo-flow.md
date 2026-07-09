# Demo Flow

## 1. Start Server


### Option A: Run Locally With Python
```powershell
C:\Users\YangMingZhou\anaconda3\python.exe -m uvicorn app.main:app --reload
```


### Option B: Run With Docker

'''powershell
docker build --pull=false -t personal-knowledge-rag .
docker run --rmm -p 8000:8000 personal-knowledge-rag
'''


### Option C: Run With Docker Compose

'''powershell
docker compose up --build
'''

For background mode:

'''powershell
docker compose up --build -d
'''

Stop Service:

'''powershell
docker compose down
'''


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


## 6. Docker Demo
If you want to run the project in Docker, follow the steps below:

'''powershell
docker build -t personal-knowledge-rag .
docker run --rm -p 8000:8000 personal-knowledge-rag
'''

Open:

'''text
https://127.0.0.1:8000/docs
'''

