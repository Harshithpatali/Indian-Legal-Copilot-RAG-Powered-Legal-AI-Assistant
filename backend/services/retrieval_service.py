from typing import List, Dict, Any
import os

from langchain_community.vectorstores import FAISS

from backend.services.embedding_service import (
    get_embeddings
)

from backend.config import settings

from backend.download_index import (
    download_faiss_files
)


def get_vectorstore():

    faiss_file = os.path.join(
        settings.FAISS_INDEX_PATH,
        "index.faiss"
    )

    pkl_file = os.path.join(
        settings.FAISS_INDEX_PATH,
        "index.pkl"
    )

    if (
        not os.path.exists(faiss_file)
        or
        not os.path.exists(pkl_file)
    ):
        print(
            "FAISS files not found. Downloading..."
        )

        download_faiss_files()

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        settings.FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def retrieve_context(
    query: str,
    k: int = 10
):
    """
    MMR Retrieval
    Used by production RAG
    """

    vectorstore = get_vectorstore()

    docs = vectorstore.max_marginal_relevance_search(
        query=query,
        k=k,
        fetch_k=50
    )

    return docs


def retrieve_with_scores(
    query: str,
    k: int = 10,
    max_score: float = 1.5
):
    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search_with_score(
        query,
        k=k
    )

    retrieved = []

    for doc, score in results:

        score = float(score)

        confidence = float(
            max(
                0.0,
                min(
                    1.0,
                    1 - (score / max_score)
                )
            )
        )

        retrieved.append(
            {
                "document": doc,
                "score": score,
                "confidence": float(
                    round(
                        confidence,
                        3
                    )
                )
            }
        )

    retrieved.sort(
        key=lambda x: x["score"]
    )

    return retrieved


def retrieve_filtered_context(
    query: str,
    k: int = 10,
    confidence_threshold: float = 0.25
):
    """
    Remove weak matches
    """

    results = retrieve_with_scores(
        query=query,
        k=k
    )

    filtered_docs = []

    for item in results:

        if item["confidence"] >= confidence_threshold:

            filtered_docs.append(
                item
            )

    return filtered_docs