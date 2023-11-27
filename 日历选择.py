#!/usr/bin/env python3
# -*- coding: utf8 -*-

from datetime import date
from datetime import timedelta

from tkcalendar import Calendar

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk


class CalendarPicker(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('400x280')
        self.today = date.today()
        self.date = None

    def date_picker(self):
        def print_sel():
            self.date = cal.selection_get()
            cal.see(date(year=self.today.year, month=self.today.month, day=self.today.day))
            self.quit()

        min_date = date(year=2018, month=1, day=21)
        max_date = self.today + timedelta(days=5)

        cal = Calendar(
            self.root, font="Arial 14", selectmode='day', locale='zh_CN',
            mindate=min_date, maxdate=max_date, disabledforeground='red',
            cursor="hand1", year=self.today.year, month=self.today.month, day=self.today.day
        )
        cal.pack(fill="both", expand=True)
        ttk.Button(self.root, text="ok", command=print_sel).pack()

    def calendar(self):
        ttk.Button(self.root, command=self.date_picker()).pack()

    def quit(self):
        self.root.destroy()

    def main(self):
        self.calendar()
        self.root.mainloop()
        print(type(self.date))
        print(f'result: {self.date}')


app = CalendarPicker()
app.main()
