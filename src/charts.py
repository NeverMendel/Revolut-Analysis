from typing import List

from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show, output_file

from src.utils import dict_keys_date_to_datetime
from statement import Statement


def money_history_chart(statements: List[Statement]):
    for st in statements:
        output_file(fr"./out/money_out_{st.currency}.html")
        balance_dict = dict_keys_date_to_datetime(st.get_list_balance_per_day_complete())

        source_balance = ColumnDataSource(data=dict(
            date=list(balance_dict.keys()),
            balance=list(balance_dict.values())
        ))
        # source_transactions = ColumnDataSource(data=dict(
        #     date=[date_to_datetime(tr.date) for tr in st.transactions],
        #     balance=[tr.balance for tr in st.transactions],
        #     tr_description=[tr.description for tr in st.transactions],
        #     tr_change=[tr.money_in - tr.money_out for tr in st.transactions]
        # ))
        chart = figure(title=f'{st.currency} over time', x_axis_label="time", y_axis_label="money",
                       x_axis_type='datetime', plot_width=1800, plot_height=700)
        chart.add_tools(HoverTool(
            tooltips=[
                ('date', '@date{%F}'),
                ('balance', '@balance{(0.00)} ' + st.currency),
                # ('description', '@tr_description')
            ],
            formatters={
                '@date': 'datetime'
            },
            mode='vline'
        ))
        chart.line('date', 'balance', source=source_balance, line_width=3)
        # chart.circle('date', 'balance', source=source_transactions, size=10)
        show(chart)
