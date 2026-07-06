from pydantic import BaseModel


class Source(
    BaseModel
):
    question: str
    score: float
    confidence: float
    content: str


class QAResponse(
    BaseModel
):
    answer: str
    confidence_score: float
    sources: list[Source]