import re

from langchain_core.documents import Document
from ingestion.load_data import load_dataset
from backend.utils.logger import logger


def clean_text(text: str) -> str:
    """
    Clean dataset artifacts.
    """

    if not isinstance(text, str):
        return ""

    text = text.replace("</s>", "")

    text = text.replace("Instruction:", "")
    text = text.replace("Response:", "")

    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def create_documents():

    df = load_dataset()

    logger.info(
        f"Original rows: {len(df)}"
    )

    df["instruction"] = (
        df["instruction"]
        .astype(str)
        .apply(clean_text)
    )

    df["response"] = (
        df["response"]
        .astype(str)
        .apply(clean_text)
    )

    # Remove duplicate questions
    df = df.drop_duplicates(
        subset=["instruction"]
    )

    logger.info(
        f"Rows after deduplication: {len(df)}"
    )

    documents = []

    for idx, row in df.iterrows():

        content = f"""
Question:
{row['instruction']}

Answer:
{row['response']}
"""

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "id": int(idx),
                    "question": row["instruction"]
                }
            )
        )

    logger.info(
        f"Documents created: {len(documents)}"
    )

    return documents