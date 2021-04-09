import csv

from statement import *


def normalize_csv(path: str):
    file = open(path, "rt")
    dataIn = file.read()
    data = dataIn
    if ";" in data:
        data = data.replace('.', '')
        data = data.replace(',', '.')
        data = data.replace(';', ',')
    for _ in range(0, 2):
        data = data.replace(', ', ',')
        data = data.replace(' , ', ',')
        data = data.replace(' ,', ',')
    file.close()
    if data != dataIn:
        file = open(path, "wt")
        file.write(data)
        file.close()


def read_statement_csv(path: str) -> Statement:
    transactions = []
    dict = csv.DictReader(open(path), delimiter=',')
    for el in dict:
        transaction = Transaction(el)
        transactions.append(transaction)

    transactions.reverse()

    statement = Statement(transactions[0].currency, transactions)
    return statement
