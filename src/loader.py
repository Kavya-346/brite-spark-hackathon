from pathlib import Path
import re


STANDARD_CLAUSE_PATTERN = re.compile(
    r"^\*\*([§Â§]?\d+\.\d+\.\d+[A-Za-z]?)\*\*(.*)$"
)

DEFINITION_CLAUSE_PATTERN = re.compile(
    r"^\*\*([§Â§]?\d+\.\d+\.\d+[A-Za-z]?)\s+(.+?)\*\*(.*)$"
)


def load_policy(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def extract_clauses(text: str) -> list[dict]:
    lines = text.splitlines()
    clauses = []

    current_clause_id = None
    current_text = []

    for line in lines:
        stripped = line.strip()

        match = STANDARD_CLAUSE_PATTERN.match(stripped)

        if match:
            if current_clause_id is not None:
                clauses.append({
                    "clause_id": current_clause_id,
                    "text": clean_clause_text(current_text)
                })

            current_clause_id = match.group(1)

            if not current_clause_id.startswith("§"):
                current_clause_id = "§" + current_clause_id

            current_text = [match.group(2)]
            continue

        match = DEFINITION_CLAUSE_PATTERN.match(stripped)

        if match:
            if current_clause_id is not None:
                clauses.append({
                    "clause_id": current_clause_id,
                    "text": clean_clause_text(current_text)
                })

            current_clause_id = match.group(1)

            if not current_clause_id.startswith("§"):
                current_clause_id = "§" + current_clause_id

            current_text = [match.group(2) + match.group(3)]
            continue

        if current_clause_id is not None:
            if stripped.startswith("#"):
                continue

            if stripped == "---":
                continue

            current_text.append(stripped)

    if current_clause_id is not None:
        clauses.append({
            "clause_id": current_clause_id,
            "text": clean_clause_text(current_text)
        })

    return clauses


def clean_clause_text(lines: list[str]) -> str:
    text = " ".join(line for line in lines if line)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def load_amendment(path: str) -> dict:
    text = Path(path).read_text(encoding="utf-8")

    issued_match = re.search(
        r"\*\*Issued:\*\*\s*(.+)",
        text
    )

    effective_match = re.search(
        r"\*\*Effective:\*\*\s*(.+)",
        text
    )

    return {
        "title": "Amendment No. 2026-01",
        "issued": issued_match.group(1).strip() if issued_match else None,
        "effective": effective_match.group(1).strip() if effective_match else None,
        "text": text
    }

def extract_amendment_clauses(text: str) -> list[dict]:
    lines = text.splitlines()
    clauses = []

    current_clause_id = None
    current_text = []

    pattern = re.compile(
        r"^\*\*(\d+\.\d+[A-Za-z]?)\*\*\s*(.*)$"
    )

    for line in lines:
        stripped = line.strip()

        match = pattern.match(stripped)

        if match:
            if current_clause_id is not None:
                clauses.append({
                    "clause_id": current_clause_id,
                    "text": clean_clause_text(current_text)
                })

            current_clause_id = match.group(1)
            current_text = [match.group(2)]
            continue

        if current_clause_id is not None:
            if stripped.startswith("#"):
                continue

            if stripped == "---":
                continue

            if stripped:
                current_text.append(stripped)

    if current_clause_id is not None:
        clauses.append({
            "clause_id": current_clause_id,
            "text": clean_clause_text(current_text)
        })

    return clauses