from datetime import datetime


class Transaction:
    """
    Credit card transaction
    """

    def __init__(self, csv_obj: dict):
        c = list(csv_obj.keys())[2]

        self.currency = c[c.index("(") + 1:c.index(")")]
        currency_string = '(' + self.currency + ')'
        self.date = datetime.strptime(csv_obj['Completed Date'], "%d %b %Y")
        self.description = csv_obj['Description']

        self.money_out = 0
        if csv_obj['Paid Out ' + currency_string] != '':
            self.money_out = float(csv_obj['Paid Out ' + currency_string])

        self.money_in = 0
        if csv_obj['Paid In ' + currency_string] != '':
            self.money_in = float(csv_obj['Paid In ' + currency_string])

        self.is_exchange = False
        self.exchange_other_currency = ''
        if csv_obj['Exchange Out'] != '' or csv_obj['Exchange In'] != '':
            self.is_exchange = True
            if csv_obj['Exchange Out'] != '':
                self.exchange_other_currency = csv_obj['Exchange Out'][:csv_obj['Exchange Out'].index(' ')]
            else:
                self.exchange_other_currency = csv_obj['Exchange In'][:csv_obj['Exchange In'].index(' ')]
        self.balance = float(csv_obj['Balance ' + currency_string])
        self.category = csv_obj['Category']
        self.notes = csv_obj['Notes']

    # def __init__(self, date, description, money_out, money_in, is_exchange, exchange_other_currency, balance, category, notes):
    #     self.date = date
    #     self.description = description
    #     self.money_out = money_out
    #     self.money_in = money_in
    #     self.is_exchange = is_exchange
    #     self.exchange_other_currency = exchange_other_currency
    #     self.balance = balance
    #     self.category = category
    #     self.notes = notes
