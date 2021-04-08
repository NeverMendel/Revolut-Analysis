from datetime import date
from typing import List, Union

from calendar_util import *
from transaction import *


class Statement:
    def __init__(self, currency: str, transactions: List[Transaction]):
        self.currency = currency
        self.transactions = transactions
        print(len(transactions))

    def check_balance(self):
        balance = 0
        for tr in self.transactions:
            balance += tr.money_in
            balance -= tr.money_out
            if round(balance, 2) != tr.balance:
                print('Problem with balance in transaction ' + str(
                    tr.date) + ' ' + tr.description + '; balance should be ' +
                      str(balance) + ' but is ' + str(tr.balance))

    def get_list_balance_per_day(self) -> List[Union[date, int]]:
        last_balance = 0
        last_date = None
        dictionary = []
        first = True
        for tr in self.transactions:
            if not first and tr.date.day > last_date.day:
                dictionary[last_date] = last_balance
            last_balance = tr.balance
            last_date = tr.date
            first = False
        return dictionary

    def get_average_balance(self, year: int) -> float:
        sum_balance = 0
        last_balance = 0
        last_date = date(year, 1, 1)
        for tr in self.transactions:
            # If first transaction of day
            if tr.date.year == year and tr.date.day > last_date.day:
                # Process last transaction
                delta = tr.date - last_date
                sum_balance += last_balance * delta.days
            last_balance = tr.balance
            last_date = tr.date
        delta = date(year, 12, 31) - last_date
        sum_balance += last_balance * delta.days
        return round(sum_balance / days_year(year))
