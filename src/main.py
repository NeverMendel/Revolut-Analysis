#!/bin/bash/python3
import argparse
from datetime import datetime

from csv_processor import normalize_csv, read_statement_csv
from charts import money_history_chart

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process csv files')
    parser.add_argument('csv', metavar='N', type=str, nargs='+',
                        help='csv filename')
    args = parser.parse_args()

    statements = []
    for el in args.csv:
        normalize_csv(el)
        statements.append(read_statement_csv(el))

    print(f"Welcome to Revolut Analysis, you have loaded {len(statements)} statements.")

    while True:
        print("""
Chose one of the following options:
  1 - Display balance over time chart
  2 - Check for errors in the statements
  3 - Get balance at given date
  4 - Get average balance in given year (calculated as the mean average of the balances at the end of the day over one year) 
  5 - Exit""")
        option = int(input())
        if option == 1:
            money_history_chart(statements)
        elif option == 2:
            for st in statements:
                tr_okay, errors = st.are_transactions_okay()
                if tr_okay:
                    print(f"No errors detected in {st.currency} statement")
                else:
                    print(f"Errors detected in {st.currency} statement\n", errors)
        elif option == 3:
            dateString = input("Insert the date you want to know the balance in the following format d/m/yyyy: ")
            inputDate = datetime.strptime(dateString, "%d/%m/%Y")
            for st in statements:
                print(f"\nBalance on {dateString} in {st.currency} statement: {st.get_balance_on_date(inputDate)} {st.currency}")
        elif option == 4:
            year = int(input("Insert the year you want to know the average balance: "))
            for st in statements:
                print(f"Average balance in {year} in {st.currency}: {st.get_average_balance(year)}")
        elif option == 5:
            break
        else:
            print("Invalid option")
