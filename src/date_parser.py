import re
from datetime import date


MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}


def extract_date(text: str):
    pattern = r"\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b"

    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return None

    day = int(match.group(1))
    month = MONTHS[match.group(2).lower()]
    year = int(match.group(3))

    try:
        return date(year, month, day)
    except ValueError:
        return None