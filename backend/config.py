from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    GROQ_API_KEY: str

    MODEL_NAME: str = "llama-3.3-70b-versatile"

    EMBEDDING_MODEL: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    TOP_K: int = 5

    DATA_PATH: str = "data/raw/train.parquet"

    FAISS_INDEX_PATH: str = (
        "vectorstore/faiss_index"
    )

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()