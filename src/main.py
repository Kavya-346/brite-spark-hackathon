from retriever import PolicyRetriever
from grounding import has_sufficient_evidence
from answer_generator import generate_answer, apply_amendments
from citation_validator import validate_citations
from date_context import DateContext
from date_parser import extract_date


retriever = PolicyRetriever()


def answer_question(question: str, date_context: DateContext):
    clauses = retriever.search(question, top_k=5)

    effective_clauses = apply_amendments(
        clauses,
        date_context.relevant_date,
        date_context.date_type
    )

    if not has_sufficient_evidence(question, effective_clauses):
        return {
            "answer": "I cannot answer this from the policy manual.",
            "evidence": []
        }

    policy_version = retriever.get_policy_version(
        date_context.relevant_date
    )

    answer = generate_answer(
        question,
        clauses,
        claim_date=date_context.relevant_date,
        date_type=date_context.date_type,
        policy_version=policy_version
    )

    citation_result = validate_citations(
        answer,
        effective_clauses
    )

    if not citation_result["all_valid"]:
        return {
            "answer": "I cannot provide a grounded answer from the policy manual.",
            "evidence": []
        }

    cited_ids = set(citation_result["valid"])

    evidence = [
        clause
        for clause in effective_clauses
        if clause["clause_id"] in cited_ids
    ]

    return {
        "answer": answer,
        "evidence": evidence,
        "claim_date": date_context.relevant_date,
        "date_type": date_context.date_type,
        "policy_version": policy_version
    }


if __name__ == "__main__":
    question = input("Ask a policy question: ")

    extracted_date = extract_date(question)

    if extracted_date:
        relevant_date = extracted_date
    else:
        date_input = input(
            "Enter the relevant date (e.g. 15 February 2026): "
        )

        relevant_date = extract_date(date_input)

        if relevant_date is None:
            print("Invalid date.")
            raise SystemExit

    date_type = input(
        "Is this a change date or determination date? "
    ).strip().lower()

    if date_type not in {"change_date", "determination_date"}:
        print("Please enter either change_date or determination_date.")
        raise SystemExit

    date_context = DateContext(
        relevant_date=relevant_date,
        date_type=date_type
    )

    result = answer_question(
        question,
        date_context
    )

    print("\nANSWER\n")
    print(result["answer"])

    print("\nPOLICY VERSION\n")
    print(result["policy_version"])

    print("\nRELEVANT DATE\n")
    print(result["claim_date"])

    print("\nDATE TYPE\n")
    print(result["date_type"])

    if result["evidence"]:
        print("\nEVIDENCE\n")

        for clause in result["evidence"]:
            print(f"{clause['clause_id']}")
            print(clause["text"])
            print()