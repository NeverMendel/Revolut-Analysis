from datetime import date, timedelta
from typing import List, Dict
from statistics import mean

from transaction import *


class Statement:
    """
    A list of transaction in a certain currency - represent a Revolut statement
    """
    def __init__(self, currency: str, transactions: List[Transaction]):
        self.currency = currency
        self.transactions = transactions

    def are_transactions_okay(self):
        balance = 0
        tr_okay = True
        errors = ""
        for tr in self.transactions:
            balance += tr.money_in
            balance -= tr.money_out
            if round(balance, 2) != tr.balance:
                errors += 'Problem with balance in transaction ' + str(tr.date) + ' ' + tr.description + '; balance should be ' + str(balance) + ' but is ' + str(tr.balance)
                tr_okay = False
        return tr_okay, errors

    def get_list_balance_per_day(self) -> Dict[date, float]:
        last_balance = 0
        last_date = None
        balance_dict = {}
        first = True
        for tr in self.transactions:
            if not first and tr.date.day > last_date.day:
                balance_dict[last_date] = last_balance
            last_balance = tr.balance
            last_date = tr.date
            first = False
        if not first:
            balance_dict[last_date] = last_balance
        return balance_dict

    def get_list_balance_per_day_complete(self) -> Dict[date, float]:
        balance_dict = self.get_list_balance_per_day()
        dates = list(balance_dict.keys())
        dates.sort()
        current_date = dates[0]
        end_date = dates[-1]
        last_value = 0

        while current_date <= end_date:
            if current_date not in balance_dict:
                balance_dict[current_date] = last_value
            last_value = balance_dict[current_date]
            current_date += timedelta(days=1)

        return balance_dict

    def get_list_balance_per_day_complete_by_year(self, year: int) -> Dict[date, float]:
        balance_dict = self.get_list_balance_per_day()
        current_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        last_value = 0

        while current_date <= end_date:
            if current_date not in balance_dict:
                balance_dict[current_date] = last_value
            last_value = balance_dict[current_date]
            current_date += timedelta(days=1)

        return balance_dict

    def get_average_balance(self, year: int) -> float:
        balance_dict = self.get_list_balance_per_day_complete_by_year(year)
        return round(mean(balance_dict.values()), 2)

    def get_balance_on_date(self, balance_date: date):
        return self.get_list_balance_per_day_complete_by_year(balance_date.year).get(balance_date)
