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


def ask_legal_question(
    question: str
):
    retrieved = retrieve_filtered_context(
        query=question,
        k=10
    )

    if not retrieved:
        return {
            "answer": "No relevant legal information was found.",
            "confidence_score": 0.0,
            "sources": []
        }

    context_chunks = []
    source_list = []
    confidence_scores = []

    for item in retrieved:

        score = float(
            item.get(
                "score",
                0.0
            )
        )

        confidence = float(
            item.get(
                "confidence",
                0.0
            )
        )

        confidence_scores.append(
            confidence
        )

        doc = item["document"]

        context_chunks.append(
            str(
                doc.page_content
            )
        )

        source_list.append(
            {
                "question": str(
                    doc.metadata.get(
                        "question",
                        ""
                    )
                ),
                "score": score,
                "confidence": confidence,
                "content": str(
                    doc.page_content[:500]
                )
            }
        )

    context = "\n\n".join(
        context_chunks
    )

    prompt = (
        load_prompt()
        .replace(
            "{context}",
            context
        )
        .replace(
            "{question}",
            question
        )
    )

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    final_confidence = float(
        round(
            sum(confidence_scores)
            / len(confidence_scores),
            3
        )
    )

    return {
        "answer": str(
            response.content
        ),
        "confidence_score": final_confidence,
        "sources": source_list
    }