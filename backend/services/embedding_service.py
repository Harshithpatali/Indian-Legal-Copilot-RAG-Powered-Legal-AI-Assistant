from functools import lru_cache

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from backend.config import settings


@lru_cache(maxsize=1)
def get_embeddings():

    print(
        "Loading embedding model..."
    )

    embeddings = (
        HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
    )

    return embeddings