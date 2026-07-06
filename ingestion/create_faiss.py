# ingestion/create_faiss.py

import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from langchain_community.vectorstores import FAISS

from ingestion.preprocess import create_documents
from backend.services.embedding_service import get_embeddings
from backend.config import settings
from backend.utils.logger import logger


# Adjust based on available RAM
BATCH_SIZE = 1000


def build_faiss():

    logger.info("Loading legal documents...")

    documents = create_documents()

    total_docs = len(documents)

    logger.info(
        f"Total documents loaded: {total_docs}"
    )

    logger.info("Loading embedding model...")

    embeddings = get_embeddings()

    logger.info("Starting batch indexing...")

    vectorstore = None

    total_batches = (
        total_docs + BATCH_SIZE - 1
    ) // BATCH_SIZE

    for batch_num, start_idx in enumerate(
        range(0, total_docs, BATCH_SIZE),
        start=1
    ):

        end_idx = min(
            start_idx + BATCH_SIZE,
            total_docs
        )

        batch_docs = documents[
            start_idx:end_idx
        ]

        logger.info(
            f"Processing batch "
            f"{batch_num}/{total_batches} "
            f"({start_idx} - {end_idx})"
        )

        try:

            if vectorstore is None:

                vectorstore = FAISS.from_documents(
                    batch_docs,
                    embeddings
                )

            else:

                vectorstore.add_documents(
                    batch_docs
                )

        except Exception as e:

            logger.error(
                f"Batch {batch_num} failed: {e}"
            )

            raise

    logger.info(
        "All batches processed successfully."
    )

    save_dir = Path(
        settings.FAISS_INDEX_PATH
    )

    save_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info(
        "Saving FAISS index..."
    )

    vectorstore.save_local(
        settings.FAISS_INDEX_PATH
    )

    logger.info(
        f"FAISS index saved to "
        f"{settings.FAISS_INDEX_PATH}"
    )

    logger.info(
        f"Indexed {total_docs} documents."
    )


if __name__ == "__main__":

    build_faiss()