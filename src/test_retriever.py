from retriever import PolicyRetriever


retriever = PolicyRetriever()

questions = [
    "How long do I have to report a change in circumstances?",
    "What is the maximum countable resource limit?",
    "How long does the Department have to determine an application?"
]

for question in questions:
    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    results = retriever.search(question)

    for result in results:
        print(
            f"\n{result['clause_id']} "
            f"(score={result['score']:.4f})"
        )
        print(result["text"])