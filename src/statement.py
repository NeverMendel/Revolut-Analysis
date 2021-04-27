from datetime import date, timedelta, datetime
from statistics import mean
from typing import List, Dict, Tuple

from transaction import Transaction
from utils import sort_dict_by_key


class Statement:
    """
    A list of transaction in a certain currency - represent a Revolut statement
    """

    def __init__(self, currency: str, transactions: List[Transaction]):
        self.currency = currency
        self.transactions = transactions

    def are_transactions_okay(self) -> Tuple[bool, str]:
        """
        Check if there isn't any error in the transactions
        :return: true if there isn't any errors, false otherwise
        :rtype: Tuple[bool, str]
        """
        balance = 0
        tr_okay = True
        errors = ""
        for tr in self.transactions:
            balance += tr.money_in
            balance -= tr.money_out
            balance = round(balance, 2)
            if balance != tr.balance:
                if not tr_okay:
                    errors += '\n'
                errors += str(
                    fr"Expected balance doesn't match with actual in transaction {tr.date.strftime('%d %b %Y')} {tr.description} balance should be {balance} {tr.currency} but is {tr.balance} {tr.currency}")
                tr_okay = False
        return tr_okay, errors

    def get_dict_balance_per_day(self) -> Dict[date, float]:
        """
        Get a dictionary with the end of the day balances for each day where there has been at least one transaction
        :return: dictionary where the date is the key and the balance is the value
        :rtype: Dict[date, float]
        """
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

    def get_dict_balance_per_day_complete(self) -> Dict[date, float]:
        """
        Get a dictionary with the end of the day balances starting from the day of the first transaction and ending
        with the day of the last transaction
        :return: dictionary where the date is the key and the balance is the value
        :rtype: Dict[date, float]
        """
        balance_dict = self.get_dict_balance_per_day()
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

    def get_dict_balance_per_day_complete_by_year(self, year: int) -> Dict[date, float]:
        """
        Get a dictionary with the end of the day balances starting from the first day of the given year and ending at
        the last day of given year
        :param year: the year you want to have a dictionary of transaction of
        :type year: int
        :return: dictionary where the date is the key and the balance is the value
        :rtype: Dict[date, float]
        """
        balance_dict = self.get_dict_balance_per_day_complete()
        res_dict = {}
        current_date = datetime(year, 1, 1).date()
        end_date = datetime(year, 12, 31).date()
        last_value = list(balance_dict.values())[-1]

        while current_date <= end_date:
            if current_date in balance_dict:
                last_value = balance_dict[current_date]
            res_dict[current_date] = last_value
            current_date += timedelta(days=1)

        return res_dict

    def get_average_balance(self, year: int) -> float:
        """
        Get average balance in a given year. Calculated as the mean average of the balances at the end of the day over
        one year
        :param year: the year you want to get the average balance of
        :type year: int
        :return: average balance
        :rtype: float
        """
        balance_dict = self.get_dict_balance_per_day_complete_by_year(year)
        return round(mean(balance_dict.values()), 2)

    def get_balance_on_date(self, balance_date: date):
        """
        Get end of day balance on given day
        :param balance_date: day you want to get the end of day balance
        :type balance_date: date
        :return: end of day balance
        :rtype: float
        """
        return self.get_dict_balance_per_day_complete_by_year(balance_date.year).get(balance_date)
