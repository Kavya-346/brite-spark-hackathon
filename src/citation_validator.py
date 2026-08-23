import re


CLAUSE_PATTERN = re.compile(r"§\d+\.\d+\.\d+[A-Za-z]*")


def extract_citations(answer: str) -> list[str]:
    return CLAUSE_PATTERN.findall(answer)


def validate_citations(
    answer: str,
    retrieved_clauses: list[dict]
) -> dict:
    citations = extract_citations(answer)

    retrieved_ids = {
        clause["clause_id"]
        for clause in retrieved_clauses
    }

    valid = [
        citation
        for citation in citations
        if citation in retrieved_ids
    ]

    invalid = [
        citation
        for citation in citations
        if citation not in retrieved_ids
    ]

    return {
        "citations": citations,
        "valid": valid,
        "invalid": invalid,
        "all_valid": len(invalid) == 0
    }