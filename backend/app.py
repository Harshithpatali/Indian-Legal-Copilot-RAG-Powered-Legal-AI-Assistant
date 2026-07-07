from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.request_models import (
    QuestionRequest
)

from backend.rag import (
    ask_legal_question
)

from backend.config import (
    settings
)

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


@app.on_event("startup")
def startup_event():

    print(
        "Application startup complete."
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


@app.get("/ping")
def ping():

    print("PING HIT")

    return {
        "status": "ok"
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


@app.get("/embedding-test")
def embedding_test():

    try:

        print("=" * 60)
        print("EMBEDDING TEST STARTED")

        from backend.services.embedding_service import (
            get_embeddings
        )

        embeddings = get_embeddings()

        print("EMBEDDING MODEL LOADED")

        return {
            "status": "embedding loaded successfully"
        }

    except Exception:

        error_trace = traceback.format_exc()

        print(error_trace)

        return {
            "error": "Embedding Test Failed",
            "traceback": error_trace
        }


@app.get("/faiss-test")
def faiss_test():

    try:

        print("=" * 60)
        print("FAISS TEST STARTED")

        from backend.services.retrieval_service import (
            get_vectorstore
        )

        vectorstore = get_vectorstore()

        print("FAISS LOADED SUCCESSFULLY")

        return {
            "status": "faiss loaded successfully"
        }

    except Exception:

        error_trace = traceback.format_exc()

        print(error_trace)

        return {
            "error": "FAISS Test Failed",
            "traceback": error_trace
        }


@app.post("/ask")
def ask(
    request: QuestionRequest
):

    try:

        print("=" * 60)
        print(
            f"QUESTION: {request.question}"
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