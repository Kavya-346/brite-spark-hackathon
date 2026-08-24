from loader import (
    load_policy,
    extract_clauses,
    extract_amendment_clauses
)


manual_text = load_policy("data/policy-manual.md")
amendment_text = load_policy("data/Amendment No. 2026-01.md")

manual_clauses = extract_clauses(manual_text)
amendment_clauses = extract_amendment_clauses(amendment_text)

print("Original manual clauses:", len(manual_clauses))
print("Amendment clauses:", len(amendment_clauses))
print("Total loaded clauses:", len(manual_clauses) + len(amendment_clauses))

print("\nAmendment clauses:\n")

for clause in amendment_clauses:
    print(clause["clause_id"])
    print(clause["text"])
    print()

