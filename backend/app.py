from fastapi import FastAPI

from backend.rag import (
    ask_legal_question
)

from backend.models.request_models import (
    QuestionRequest
)

app = FastAPI(
    title="Indian Legal Research Copilot",
    version="1.0.0"
)


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask(
    request: QuestionRequest
):

    return ask_legal_question(
        request.question
    )