import re


def normalize_words(text):
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    normalized = []

    for word in words:
        if word.endswith("ies"):
            word = word[:-3] + "y"
        elif word.endswith("s") and len(word) > 3:
            word = word[:-1]

        normalized.append(word)

    return normalized


def has_sufficient_evidence(
    question: str,
    clauses: list[dict],
    threshold: float = 0.54
) -> bool:

    if not clauses:
        return False

    best_score = max(
        clause.get("score", 0.0)
        for clause in clauses
    )

    if best_score < threshold:
        return False

    semantic_clauses = [
        clause
        for clause in clauses
        if clause.get("score", 0.0) > 0.0
    ]

    referenced_clauses = [
        clause
        for clause in clauses
        if clause.get("score", 0.0) == 0.0
    ]

    if referenced_clauses:
        semantic_text = " ".join(
            clause["text"].lower()
            for clause in semantic_clauses
        )

        referenced_text = " ".join(
            clause["text"].lower()
            for clause in referenced_clauses
        )

        combined_text = semantic_text + " " + referenced_text
    else:
        combined_text = " ".join(
            clause["text"].lower()
            for clause in clauses[:3]
        )

    question_words = normalize_words(question)

    stop_words = {
        "what", "is", "are", "the", "a", "an", "of",
        "to", "do", "i", "have", "how", "long", "can",
        "does", "for", "in", "on", "and", "or", "after",
        "someone", "applicable", "there", "any", "other",
        "about", "my", "me", "their", "this", "that"
    }

    important_words = {
        word for word in question_words
        if word not in stop_words
    }


    evidence_words = set(normalize_words(combined_text))

    matched_words = {
        word for word in important_words
        if word in evidence_words
    }

    if "maximum" in important_words or "limit" in important_words:
        if "exceed" in evidence_words:
            matched_words.add("maximum")
            matched_words.add("limit")

    if not important_words:
        return False

    coverage = len(matched_words) / len(important_words)

    if coverage < 0.30:
        return False

    corpus_terms = set()

    for clause in clauses:
        corpus_terms.update(
            normalize_words(clause["text"])
        )

    unknown_words = important_words - corpus_terms

    if len(unknown_words) >= 2 and len(matched_words) < 3:
        if not (
            ("maximum" in important_words or "limit" in important_words)
            and "exceed" in evidence_words
        ):
            return False

    return True