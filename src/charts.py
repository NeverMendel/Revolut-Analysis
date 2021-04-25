from typing import List

from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show, output_file

from statement import Statement


# def create_gui(statements: List[Statement]):
#     window = Tk()
#
#     in_button = Button(window, text="Money history chart", command=lambda: money_history_chart(statements))
#     in_button.pack()
#
#     info_button = Button(window, text="Display general information about your statements",
#                          command=lambda: info_screen(statements))
#     info_button.pack()
#
#     mainloop()


def money_history_chart(statements: List[Statement]):
    output_file("./out/money_out.html")
    for st in statements:
        dictionary = st.get_list_balance_per_day_complete()
        source = ColumnDataSource(data=dict(
            date=list(dictionary.keys()),
            money=list(dictionary.values())
        ))
        # TOOLTIPS = [
        #     ("index", "$index"),
        #     ('date', '$x'),
        # ]
        chart = figure(title=f'{st.currency} over time', x_axis_label="time", y_axis_label="money",
                       x_axis_type='datetime', plot_width=1800, plot_height=700)
        chart.add_tools(HoverTool(
            tooltips=[
                ('date', '@date{%F}'),
                ('money', '@money{%0.2f}')
            ],
            formatters={
                'date': 'datetime',
                'money': 'printf'
            },
            mode='vline'
        ))
        chart.line('date', 'money', source=source, line_width=3)
        show(chart)


def info_screen(statements: List[Statement]):
    print('a')
