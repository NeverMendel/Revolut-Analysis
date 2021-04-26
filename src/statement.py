from datetime import date, timedelta, datetime
from statistics import mean
from typing import List, Dict

from src.utils import sort_dict_by_key
from transaction import Transaction


class Statement:
    """
    A list of transaction in a certain currency - represent a Revolut statement
    """

    def __init__(self, currency: str, transactions: List[Transaction]):
        self.currency = currency
        self.transactions = transactions

    def get_transaction_dict(self) -> Dict[date, Transaction]:
        tr_dict = {}
        for tr in self.transactions:
            tr_dict[tr.date] = tr
        return tr_dict

    def are_transactions_okay(self):
        balance = 0
        tr_okay = True
        errors = ""
        for tr in self.transactions:
            balance += tr.money_in
            balance -= tr.money_out
            balance = round(balance, 2)
            if balance != tr.balance:
                errors += str(
                    fr"Expected balance doesn't match with actual in transaction {tr.date.strftime('%d %b %Y')} {tr.description} balance should be {balance} {tr.currency} but is {tr.balance} {tr.currency}")
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

        return sort_dict_by_key(balance_dict)

    def get_list_balance_per_day_complete_by_year(self, year: int) -> Dict[date, float]:
        balance_dict = self.get_list_balance_per_day_complete()
        res_dict = {}
        current_date = datetime(year, 1, 1).date()
        end_date = datetime(year, 12, 31).date()
        last_value = 0

        while current_date <= end_date:
            if current_date in balance_dict:
                last_value = balance_dict[current_date]
            res_dict[current_date] = last_value
            current_date += timedelta(days=1)

        return res_dict

    def get_average_balance(self, year: int) -> float:
        balance_dict = self.get_list_balance_per_day_complete_by_year(year)
        return round(mean(balance_dict.values()), 2)

    def get_balance_on_date(self, balance_date: date):
        return self.get_list_balance_per_day_complete_by_year(balance_date.year).get(balance_date)
