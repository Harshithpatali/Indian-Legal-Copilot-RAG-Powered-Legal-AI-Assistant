from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from backend.config import settings


def get_embeddings():

    embeddings = (
        HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
    )

    return embeddings