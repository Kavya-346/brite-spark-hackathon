from loader import load_policy, extract_clauses


text = load_policy("data/policy-manual.md")
clauses = extract_clauses(text)

clause_ids = [clause["clause_id"] for clause in clauses]

duplicates = {
    clause_id
    for clause_id in clause_ids
    if clause_ids.count(clause_id) > 1
}

print("Total clauses:", len(clauses))
print("Unique clause IDs:", len(set(clause_ids)))

if duplicates:
    print("\nDuplicate clause IDs found:")
    for clause_id in sorted(duplicates):
        print(clause_id)
else:
    print("\nNo duplicate clause IDs found.")

required_clauses = [
    "§1.1.1",
    "§1.4.1",
    "§2.1.1",
    "§4.3.2",
    "§6.4.1",
    "§9.1.4",
    "§10.5.1",
    "§11.1.1",
    "§12.3.3"
]

print("\nRequired clause checks:")

for clause_id in required_clauses:
    found = clause_id in clause_ids
    print(f"{clause_id}: {'FOUND' if found else 'MISSING'}")