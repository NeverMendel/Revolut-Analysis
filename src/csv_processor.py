import csv

from statement import Statement
from transaction import Transaction

import re


def normalize_csv(path: str):
    file = open(path, "rt")
    data_in = file.read()
    data = data_in
    data = re.sub(r"(\d+),(\d)", r"\1\2", data)
    if ";" in data:
        data = data.replace('.', '')
        data = data.replace(',', '.')
        data = data.replace(';', ',')
    for _ in range(0, 2):
        data = data.replace(', ', ',')
        data = data.replace(' , ', ',')
        data = data.replace(' ,', ',')
    file.close()
    if data != data_in:
        file = open(path, "wt")
        file.write(data)
        file.close()


def read_statement_csv(path: str) -> Statement:
    transactions = []
    tr_dict = csv.DictReader(open(path), delimiter=',')
    for el in tr_dict:
        transaction = Transaction(el)
        transactions.append(transaction)

    transactions.reverse()

    statement = Statement(transactions[0].currency, transactions)
    return statement
