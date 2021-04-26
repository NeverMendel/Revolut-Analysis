from datetime import date, datetime
from typing import Optional, Dict


def date_to_datetime(d: date, hours: Optional[int] = 0, minutes: Optional[int] = 0,
                     seconds: Optional[int] = 0) -> datetime:
    return datetime(d.year, d.month, d.day, hours, minutes, seconds)


def dict_keys_date_to_datetime(date_dict: Dict[date, float]) -> Dict[datetime, float]:
    datetime_dict = {}
    for key in date_dict.keys():
        datetime_dict[date_to_datetime(key)] = date_dict[key]
    return datetime_dict


def sort_dict_by_key(input_dict: Dict) -> Dict:
    return {k: input_dict[k] for k in sorted(input_dict)}
