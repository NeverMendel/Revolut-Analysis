def is_leap(year: int) -> bool:
    return year % 4 == 0 or year % 100 == 0 or year % 400 == 0


def days_year(year: int) -> int:
    if is_leap(year):
        return 366
    return 365
