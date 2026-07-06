from huggingface_hub import hf_hub_download
import os


def download_faiss_files():

    REPO_ID = "Harshith003/legal-copilot-faiss"

    os.makedirs(
        "vectorstore/faiss_index",
        exist_ok=True
    )

    hf_hub_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        filename="index.faiss",
        local_dir="vectorstore/faiss_index"
    )

    hf_hub_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        filename="index.pkl",
        local_dir="vectorstore/faiss_index"
    )

    print(
        "FAISS files downloaded successfully"
    )