import json

from retriever import PolicyRetriever
from grounding import has_sufficient_evidence


TEST_CASES = [
    {
        "id": "Q1",
        "question": "How long do I have to report a change in circumstances?",
        "expected": ["§4.3.2"],
        "should_refuse": False
    },
    {
        "id": "Q2",
        "question": "What is the maximum countable resource limit?",
        "expected": ["§2.4.1"],
        "should_refuse": False
    },
    {
        "id": "Q3",
        "question": "How long does the Department have to determine an application?",
        "expected": ["§8.3.1"],
        "should_refuse": False
    },
    {
        "id": "Q4",
        "question": "What income is disregarded for a dependent child?",
        "expected": ["§6.4.1"],
        "should_refuse": False
    },
    {
        "id": "Q5",
        "question": "How much is the sanction for a first sanction?",
        "expected": ["§10.5.2"],
        "should_refuse": False
    },
    {
        "id": "Q6",
        "question": "What is the reporting deadline for a change of circumstances and are there any other provisions about the reporting period?",
        "expected": ["§4.3.2", "§9.1.4"],
        "should_refuse": False
    },
    {
        "id": "Q7",
        "question": "How long do I have to appeal after the review outcome?",
        "expected": ["§12.1.2"],
        "should_refuse": False
    },
    {
        "id": "Q8",
        "question": "Can an applicant submit alternative evidence if they cannot provide a specified document?",
        "expected": ["§8.2.2"],
        "should_refuse": False
    },
    {
        "id": "Q9",
        "question": "What is the weather in Calder County tomorrow?",
        "expected": [],
        "should_refuse": True
    },
    {
        "id": "Q10",
        "question": "What are the tax rates applicable to household income?",
        "expected": [],
        "should_refuse": True
    }
]


def run_evaluation():
    retriever = PolicyRetriever()

    passed = 0
    results = []

    for test in TEST_CASES:
        retrieved = retriever.search(test["question"], top_k=5)

        retrieved_ids = [
            clause["clause_id"]
            for clause in retrieved
        ]

        if test["should_refuse"]:
            test_passed = not has_sufficient_evidence(
                test["question"],
                retrieved
            )
        else:
            test_passed = any(
                clause_id in retrieved_ids
                for clause_id in test["expected"]
            )

        if test_passed:
            passed += 1

        results.append({
            "id": test["id"],
            "question": test["question"],
            "expected_clauses": test["expected"],
            "retrieved_clauses": retrieved_ids,
            "should_refuse": test["should_refuse"],
            "passed": test_passed
        })

    total = len(TEST_CASES)
    failed = total - passed
    pass_rate = round((passed / total) * 100, 1)

    report = {
        "evaluation": "Grounded Answer",
        "total_questions": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "results": results
    }

    with open("evaluation_results.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("=" * 70)
    print("GROUNDED ANSWER EVALUATION")
    print("=" * 70)

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"

        print(f"\n{result['id']}: {status}")
        print(f"Question: {result['question']}")
        print(f"Expected: {result['expected_clauses']}")
        print(f"Retrieved: {result['retrieved_clauses']}")

    print("\n" + "=" * 70)
    print(f"RESULT: {passed}/{total} passed")
    print(f"PASS RATE: {pass_rate}%")
    print("=" * 70)
    print("\nSaved to evaluation_results.json")


if __name__ == "__main__":
    run_evaluation()