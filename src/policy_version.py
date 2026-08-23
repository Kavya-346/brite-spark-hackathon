from datetime import date


AMENDMENT_EFFECTIVE_DATE = date(2026, 3, 1)


def get_policy_version(relevant_date: date) -> str:
    if relevant_date < AMENDMENT_EFFECTIVE_DATE:
        return "original"

    return "amended"


def get_reporting_period(change_date: date) -> int:
    if change_date < AMENDMENT_EFFECTIVE_DATE:
        return 10

    return 14


def get_earnings_disregard(determination_date: date) -> int:
    if determination_date < AMENDMENT_EFFECTIVE_DATE:
        return 120

    return 175


def get_sanction_percentage(determination_date: date) -> int:
    if determination_date < AMENDMENT_EFFECTIVE_DATE:
        return 20

    return 15


def get_income_thresholds(determination_date: date) -> dict:
    if determination_date < AMENDMENT_EFFECTIVE_DATE:
        return {
            1: 1180,
            2: 1590,
            3: 2000,
            4: 2410,
            5: 2820,
            "additional": 410
        }

    return {
        1: 1225,
        2: 1650,
        3: 2075,
        4: 2500,
        5: 2925,
        "additional": 425
    }