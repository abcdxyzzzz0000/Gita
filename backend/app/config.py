from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://postgres:root@localhost:5432/gita"
    database_url_sync: str = "postgresql://postgres:root@localhost:5432/gita"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 1440  # 24 hours

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/auth/google/callback"

    # RAG / AI
    faiss_index_path: str = "data/faiss_index.bin"
    faiss_mapping_path: str = "data/faiss_mapping.json"
    embedding_model: str = "all-MiniLM-L6-v2"
    ollama_model: str = "mistral:7b"
    ollama_base_url: str = "http://localhost:11434"
    rag_context_size: int = 3
    rag_max_tokens: int = 500
    rag_temperature: float = 0.7

    # App
    debug: bool = True
    app_name: str = "Bhagavad Gita Learning API"
    api_prefix: str = "/api"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
