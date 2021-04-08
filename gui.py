from tkinter import *
from typing import List

from statement import Statement


def create_gui(statements: List[Statement]):
    window = Tk()

    in_button = Button(window, text="Display money In chart", command=lambda: money_in_chart(statements))
    in_button.pack()

    out_button = Button(window, text="Display money Out chart", command=lambda: money_out_chart(statements))
    out_button.pack()

    info_button = Button(window, text="Display general information about your statements",
                         command=lambda: info_screen(statements))
    info_button.pack()

    mainloop()


def money_in_chart(statements: List[Statement]):
    print('a')


def money_out_chart(statements: List[Statement]):
    print('a')


def info_screen(statements: List[Statement]):
    print('a')
