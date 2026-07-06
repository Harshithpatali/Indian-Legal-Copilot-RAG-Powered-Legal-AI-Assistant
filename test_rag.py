from backend.rag import (
    ask_legal_question
)

result = ask_legal_question(
    "What is Section 420 IPC?"
)

print("\nANSWER\n")
print(result["answer"])

print("\nSOURCES\n")

for source in result["sources"]:

    print(
        source["question"]
    )