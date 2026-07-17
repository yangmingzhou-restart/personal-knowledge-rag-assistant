from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Basic information
    app_name: str = "Personal Knowledge RAG Assistant"
    app_env: str = "development"

    # Database configuration
    database_path: Path = Path("data/app.sqlite3")
    vector_store_provider: str = "sqlite"  # qdrant

    # Embedding configuration
    embedding_provider: str = "fake"
    local_embedding_model: str = (
        r"D:\AI创业\AI模型\embedding-models\BAAI\bge-small-zh-v1.5"
    )

    # Vector store configuration
    qdrant_url: str = "http://127.0.0.1:6333"
    qdrant_collection: str = "personal_knowlegde_chunks"

    # Reranker configuration
    reranker_provider: str = "keyword"
    reranker_model: str = (
        r"D:\AI创业\AI模型\rerank-model\BAAI\bge-reranker-base"
    )

    # LLM configuration
    llm_provider: str = "fake"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5:3b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
