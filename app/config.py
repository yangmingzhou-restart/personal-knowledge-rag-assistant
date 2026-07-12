from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Personal Knowledge RAG Assistant"
    app_env: str = "development"

    database_path: Path = Path("data/app.sqlite3")
    
    embedding_provider: str = "fake"
    local_embedding_model: str = (
        r"D:\AI创业\AI模型\embedding-models\BAAI\bge-small-zh-v1.5"
    )

    llm_provider: str = "fake"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5:3b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
