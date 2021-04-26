#!/usr/bin/env python3
import argparse
from datetime import datetime
from typing import Optional

from charts import balance_chart
from csv_processor import read_statement_csv

menu_description = """
Chose one of the following options:
  1 - Display balance over time chart
  2 - Check for errors in the statements
  3 - Get end of day balance at given date
  4 - Get average balance in a given year (calculated as the mean average of the balances at the end of the day over one year)
  5 - Exit"""


def menu_option(option: int, arg: Optional) -> bool:
    if option == 1:
        if arg:
            balance_chart(statements, True)
        else:
            balance_chart(statements, False)
    elif option == 2:
        for st in statements:
            tr_okay, errors = st.are_transactions_okay()
            if tr_okay:
                print(f"No errors detected in {st.currency} statement")
            else:
                print(f"Errors detected in {st.currency} statement:")
                print(errors)
    elif option == 3:
        if arg:
            date_string = arg
        else:
            date_string = input("Insert the date you want to know the balance in the following format d/m/yyyy: ")
        input_date = datetime.strptime(date_string, "%d/%m/%Y").date()
        print(f"End of day balance on {date_string}:")
        for st in statements:
            print(f"{st.currency} statement: {st.get_balance_on_date(input_date)} {st.currency}")
    elif option == 4:
        if arg:
            year = arg
        else:
            year = int(input("Insert the year you want to know the average balance: "))
        print(f"Average balance in {year}")
        for st in statements:
            print(f"{st.currency} statement: {st.get_average_balance(year)} {st.currency}")
    elif option == 5:
        return True
    else:
        print("Invalid option")
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse Revolut transactions.')
    parser.add_argument('csv', metavar='N', type=str, nargs='+',
                        help='statement filename')
    parser.add_argument('--show-chart', action="store_true",
                        help='display the balance charts')
    parser.add_argument('--save-chart', action="store_true",
                        help='save the balance charts in the out folder')
    parser.add_argument('--check-errors', action="store_true",
                        help='check for errors in the statements')
    previous_year = datetime.today().year - 1
    parser.add_argument('--get-balance', nargs='?', type=str, const=fr"31/12/{previous_year}",
                        help='get balance at given date; default: last day of last year')
    parser.add_argument('--average-balance', nargs='?', type=int, const=previous_year, help='get mean average balance in a given year')
    args = parser.parse_args()

    statements = []
    for el in args.csv:
        statements.append(read_statement_csv(el))

    print(
        f"Welcome to Revolut Analysis, you have loaded {len(statements)} statements ({', '.join([st.currency for st in statements])}).")

    if args.show_chart:
        menu_option(1, False)
    elif args.save_chart:
        menu_option(1, True)
    elif args.check_errors:
        menu_option(2, None)
    elif args.get_balance:
        menu_option(3, args.get_balance)
    elif args.average_balance:
        menu_option(4, args.average_balance)
    else:
        while True:
            print(menu_description)
            option = int(input())
            end = menu_option(option, None)
            if end:
                break
