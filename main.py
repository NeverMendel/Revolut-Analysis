import argparse

from csv_processor import *
from gui import create_gui

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
        st.check_balance()
        print(st.get_average_balance(2019))
        print(st.get_list_balance_per_day())

    create_gui(statements)
