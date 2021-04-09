from datetime import date, datetime
from typing import Optional


def date_to_datetime(d: date, hours: Optional[int] = 0, minutes: Optional[int] = 0, seconds: Optional[int] = 0) -> datetime:
    return datetime(d.year, d.month, d.day, hours, minutes, seconds)
