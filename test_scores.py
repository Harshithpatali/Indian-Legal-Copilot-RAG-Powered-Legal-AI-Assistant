# test_scores.py

from backend.services.retrieval_service import (
    retrieve_with_scores
)

query = "What is Article 19?"

results = retrieve_with_scores(
    query=query,
    k=10
)

for rank, item in enumerate(results, 1):

    print("\n")
    print("=" * 80)

    print(
        f"Rank: {rank}"
    )

    print(
        f"Score: {item['score']}"
    )

    print(
        f"Confidence: {item['confidence']}"
    )

    print(
        item["document"]
        .metadata["question"]
    )