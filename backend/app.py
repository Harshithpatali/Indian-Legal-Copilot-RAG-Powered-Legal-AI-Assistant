from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.request_models import QuestionRequest
from backend.rag import ask_legal_question

from backend.download_index import download_faiss_files

import os


app = FastAPI(
    title="Indian Legal Research Copilot",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():

    os.makedirs(
        "vectorstore/faiss_index",
        exist_ok=True
    )

    faiss_file = (
        "vectorstore/faiss_index/index.faiss"
    )

    pkl_file = (
        "vectorstore/faiss_index/index.pkl"
    )

    if (
        not os.path.exists(faiss_file)
        or
        not os.path.exists(pkl_file)
    ):
        print(
            "Downloading FAISS files from Hugging Face..."
        )

        download_faiss_files()

        print(
            "FAISS download completed."
        )
    else:
        print(
            "FAISS files already exist."
        )


@app.get("/")
def root():

    return {
        "message": "Indian Legal Research Copilot API Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask(
    request: QuestionRequest
):

    result = ask_legal_question(
        request.question
    )

    return result