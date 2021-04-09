#!/bin/bash/python3
import argparse

from csv_processor import *
from gui import create_gui, money_history_chart

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process csv files')
    parser.add_argument('csv', metavar='N', type=str, nargs='+',
                        help='csv filename')
    args = parser.parse_args()

    statements = []
    for el in args.csv:
        normalize_csv(el)
        statements.append(read_statement_csv(el))

    for st in statements:
        st.are_transactions_okay()
        print("Balance ", st.get_average_balance(2021))
        # for tr in st.transactions:
        #     print(tr.date, " ", tr.balance)
        # print(st.get_list_balance_per_day())

    money_history_chart(statements)
    create_gui(statements)
