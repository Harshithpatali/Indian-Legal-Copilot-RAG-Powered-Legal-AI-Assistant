from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.request_models import QuestionRequest
from backend.rag import ask_legal_question

from backend.download_index import download_faiss_files
from backend.config import settings

import os
import traceback


app = FastAPI(
    title="Indian Legal Research Copilot",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    print("PING HIT")
    return {"status": "ok"}



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

        try:

            download_faiss_files()

            print(
                "FAISS download completed."
            )

        except Exception as e:

            print(
                f"FAISS download failed: {e}"
            )

            raise

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


@app.get("/env-test")
def env_test():

    return {
        "groq_exists": bool(
            settings.GROQ_API_KEY
        ),
        "model": settings.MODEL_NAME,
        "embedding": settings.EMBEDDING_MODEL,
        "faiss_path": settings.FAISS_INDEX_PATH
    }


@app.post("/ask")
def ask(
    request: QuestionRequest
):

    try:

        print("=" * 60)
        print(
            "QUESTION:",
            request.question
        )

        result = ask_legal_question(
            request.question
        )

        print(
            "QUESTION COMPLETED"
        )

        return result

    except Exception:

        error_trace = traceback.format_exc()

        print(error_trace)

        return {
            "error": "Internal Error",
            "traceback": error_trace
        }