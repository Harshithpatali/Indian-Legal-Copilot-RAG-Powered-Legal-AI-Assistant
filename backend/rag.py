from pathlib import Path

from backend.services.llm_service import (
    get_llm
)

from backend.services.retrieval_service import (
    retrieve_filtered_context
)

PROMPT_PATH = Path(
    "backend/prompts/legal_qa_prompt.txt"
)


def load_prompt():
    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


def ask_legal_question(question: str):

    print("STEP 1")

    retrieved = retrieve_filtered_context(
        query=question,
        k=10
    )

    print("STEP 2")

    return {
        "answer": "retrieval works",
        "retrieved_count": len(retrieved)
    }