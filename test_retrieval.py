from backend.services.retrieval_service import (
    retrieve_context
)

docs = retrieve_context(
    "What is Section 420 IPC?"
)

for i, doc in enumerate(docs):

    print(
        "\n",
        "="*50
    )

    print(
        f"Result {i+1}"
    )

    print(
        doc.page_content[:1000]
    )