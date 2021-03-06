import csv
import io
import re

from statement import Statement
from transaction import Transaction


def get_csv_normalized(path: str) -> str:
    """
    Normalize Revolut statement to standard csv format
    :param path: path of Revolut statement
    :type path: str
    :return: statement normalized
    :rtype: str
    """
    file = open(path, "rt")
    data = file.read()
    data = re.sub(r"(\d+),(\d)", r"\1\2", data)
    # if ";" in data:
    #     data = data.replace('.', '')
    #     data = data.replace(',', '.')
    #     data = data.replace(';', ',')
    for _ in range(0, 2):
        data = data.replace(', ', ',')
        data = data.replace(' , ', ',')
        data = data.replace(' ,', ',')
    file.close()
    return data


def read_statement_csv(path: str) -> Statement:
    """
    Get Statement object from Revolut statement path
    :param path: path of Revolut statement
    :type path: str
    :return: statement object
    :rtype: Statement
    """
    transactions = []
    tr_dict = csv.DictReader(io.StringIO(get_csv_normalized(path)), delimiter=',')
    for el in tr_dict:
        transaction = Transaction(el)
        transactions.append(transaction)

    transactions.reverse()

    statement = Statement(transactions[0].currency, transactions)
    return statement
