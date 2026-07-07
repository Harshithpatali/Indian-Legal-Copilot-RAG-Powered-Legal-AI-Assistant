from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from backend.config import settings


@lru_cache(maxsize=1)
def get_embeddings():

    print("STEP 1: Starting embedding load", flush=True)

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL
    )

    print("STEP 2: Embedding model loaded", flush=True)

    return embeddings