from tkinter import *
from typing import List

from bokeh.models import DatetimeTickFormatter, HoverTool
from bokeh.plotting import figure, show, output_file, save

from src.utils import date_to_datetime
from statement import Statement


def create_gui(statements: List[Statement]):
    window = Tk()

    in_button = Button(window, text="Money history chart", command=lambda: money_history_chart(statements))
    in_button.pack()

    info_button = Button(window, text="Display general information about your statements",
                         command=lambda: info_screen(statements))
    info_button.pack()

    mainloop()


def money_history_chart(statements: List[Statement]):
    output_file("./out/money_out.html")
    for st in statements:
        TOOLTIPS = [
            ("money", "$x"),
            ("date", "$y")
        ]
        chart = figure(title="Money over time", x_axis_label="time", y_axis_label="money", x_axis_type='datetime', plot_width=1800, plot_height=700)
        dictionary = st.get_list_balance_per_day()
        x = list(dictionary.keys())
        y = list(dictionary.values())
        chart.add_tools(HoverTool(
            tooltips=[
                ( 'date',   '@date{%F}'            ),
                ( 'money',  '$y' )
            ],

            formatters={
                '@date'        : 'datetime', # use 'datetime' formatter for '@date' field
            },

            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode='vline'
        ))
        chart.step(x, y, legend_label="Currency", line_width=3)
        chart.xaxis.formatter = DatetimeTickFormatter(days=["%m/%d"])
        print(x)
        print("y", y)
        show(chart)


def info_screen(statements: List[Statement]):
    print('a')
