from dataclasses import dataclass
from datetime import date


@dataclass
class DateContext:
    relevant_date: date
    date_type: str

    def is_amended(self) -> bool:
        return self.relevant_date >= date(2026, 3, 1)