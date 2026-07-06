try:
    from langchain_groq import ChatGroq  # type: ignore[import]
except ImportError as exc:
    raise ImportError(
        "langchain_groq is required for LLM service. Install it with pip."
    ) from exc

from backend.config import settings


def get_llm():

    llm = ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.MODEL_NAME,
        temperature=0.1,
        max_tokens=2048
    )

    return llm