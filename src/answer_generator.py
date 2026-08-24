import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=API_KEY)


AMENDMENTS_PATH = Path("data/amendments.json")

with open(AMENDMENTS_PATH, "r", encoding="utf-8") as file:
    AMENDMENTS = json.load(file)


SYSTEM_PROMPT = """
You are a policy assistant for the Calder County Household Support Program.

The supplied policy clauses and supplied amendment information are the ONLY authority.

Rules:

1. Answer only from the supplied policy material.
2. Never use outside knowledge.
3. Every substantive policy claim must include a clause citation such as §4.3.2.
4. Do not invent policy, deadlines, amounts, eligibility rules, or procedures.
5. Apply Amendment No. 2026-01 according to its effective date and transitional provisions.
6. The relevant date and date type supplied by the system determine which amendment rules apply.
7. For reporting-of-change questions, distinguish the date the change occurred from the determination date.
8. For amendments governed by determination date, apply the amended value when the determination is on or after 1 March 2026.
9. For reporting amendments, apply the amended reporting period only when the change occurred on or after 1 March 2026.
10. If the supplied material does not contain enough information to answer the question, say:
    "I cannot answer this from the policy manual."
11. If relevant clauses conflict, explicitly identify the conflict and cite each conflicting clause.
12. Do not silently resolve a contradiction using general knowledge.
13. Keep the answer concise and clear.
14. Preserve uncertainty where the policy itself is uncertain.
"""
def apply_amendments(clauses, claim_date, date_type):
    from datetime import date

    if claim_date is None:
        return clauses

    amendment_date = date(2026, 3, 1)

    updated_clauses = []

    for clause in clauses:
        updated = clause.copy()
        clause_id = clause["clause_id"]
        text = clause["text"]

        if date_type == "determination_date" and claim_date >= amendment_date:

            if clause_id == "§6.4.1":
                text = text.replace(
                    "$120 per month",
                    "$175 per month"
                )

            elif clause_id == "§6.6.1":
                text = text.replace("$1,180", "$1,225")
                text = text.replace("$1,590", "$1,650")
                text = text.replace("$2,000", "$2,075")
                text = text.replace("$2,410", "$2,500")
                text = text.replace("$2,820", "$2,925")
                text = text.replace("+ $410", "+ $425")

            elif clause_id == "§10.5.2":
                text = text.replace(
                    "20 per cent",
                    "15 per cent"
                )

        if date_type == "change_date":

            if claim_date >= amendment_date:

                if clause_id == "§4.3.2":
                    text = text.replace(
                        "10 calendar days",
                        "14 calendar days"
                    )

                elif clause_id == "§9.1.4":
                    text = text.replace(
                        "30 calendar days",
                        "14 calendar days"
                    )

            else:

                if clause_id == "§4.3.2":
                    text = text.replace(
                        "14 calendar days",
                        "10 calendar days"
                    )

                elif clause_id == "§9.1.4":
                    text = text.replace(
                        "14 calendar days",
                        "30 calendar days"
                    )

        updated["text"] = text
        updated_clauses.append(updated)

    if date_type == "determination_date" and claim_date >= amendment_date:
        updated_clauses.append({
            "clause_id": "§10.5.3A",
            "text": (
                "A sanction must not be imposed in respect of a failure "
                "to report where the change of circumstances in question "
                "would have increased the award."
            ),
            "score": 0.0
        })

    return updated_clauses

def generate_answer(
    question: str,
    clauses: list[dict],
    claim_date=None,
    date_type="determination_date",
    policy_version="Original manual"
) -> str:

    effective_clauses = apply_amendments(
        clauses,
        claim_date,
        date_type
    )

    evidence = "\n\n".join(
        f"POLICY CLAUSE {clause['clause_id']}:\n{clause['text']}"
        for clause in effective_clauses
    )


    prompt = f"""
{SYSTEM_PROMPT}

Question:
{question}

Relevant date:
{claim_date}

Date type:
{date_type}

Policy version:
{policy_version}

Relevant policy clauses:
{evidence}

IMPORTANT:
The policy clauses above have already been adjusted for the applicable amendment.
Treat those effective clause texts as authoritative for this question.
If an effective clause contains "$175 per month", the answer must state "$175 per month".
Do not omit a specific amount that directly answers the question.

The "Relevant policy clauses" above have already been transformed
by the application according to the supplied relevant date and date type.

Treat those effective clause texts as the ONLY authoritative policy text.

Do not independently apply, reinterpret, or override amendment dates.

Do not use amendment metadata to change the effective clause text.

If the effective clause says "10 calendar days", answer 10 calendar days.
If the effective clause says "14 calendar days", answer 14 calendar days.

The supplied date type is authoritative:
- change_date means the date the change of circumstances occurred.
- determination_date means the date the determination was made.

Do not apply a change_date amendment to a determination_date question.
Do not apply a determination_date amendment to a change_date question.

If the question asks for a specific amount, percentage, threshold, or
deadline, extract that exact value from the effective clause and state it.

Do not give a general statement when the policy contains a specific
value that answers the question.

For example, if the effective §6.4.1 contains "$175 per month", the
answer must explicitly state "$175 per month".

Answer the question using ONLY the supplied effective policy clauses.

Every substantive policy claim must include the relevant original policy clause citation.

If an amendment changes a clause, cite the underlying policy clause that the amendment changes.

Do not mention information that is not supported by the supplied material.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text