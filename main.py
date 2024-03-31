import os
import random
import socket
import time
from tkinter import *
from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

import psutil
from munch import DefaultMunch

hostname = socket.gethostname()

temp = {
    "utils": [
        {
            "title": "Packets Sent",
            "body": lambda: psutil.net_io_counters().packets_sent
        },
        {
            "title": "Packets Received",
            "body": lambda: psutil.net_io_counters().packets_recv,
        },
        {
            "title": "Incoming Packets",
            "body": lambda: psutil.net_io_counters().dropin,
        },
        {
            "title": "Out coming Packets",
            "body": lambda: psutil.net_io_counters().dropout,
        },
        {
            "title": "Host name",
            "body": lambda: hostname
        },
        {
            "title": "IPv4",
            "body": lambda: psutil.net_connections()[0].laddr.ip
        },
        {
            "title": "Free memory",
            "body": lambda: f"{psutil.virtual_memory().percent}%",
        },
        {
            "title": "Batery",
            "body": lambda: f"{psutil.sensors_battery().percent}%",
        },
    ]
}


class Main(tk.Tk):
    COLUMNS = 4
    ROWS = 2
    grid_count = 0

    def _print_div(self, title: str, funct, row: int, column: int) -> None:
        self.lb_title.append(tk.Label(text=title))
        self.lb_title[self.grid_count].grid(column=column, row=row, sticky="n", padx=(50, 100))

        self.lb_body_callback.append((StringVar(), funct))
        self.lb_body_callback[self.grid_count][0].set(self.lb_body_callback[self.grid_count][1]())

        self.lb_body.append(tk.Label(textvariable=self.lb_body_callback[self.grid_count][0]))
        self.lb_body[self.grid_count].grid(column=column, row=row, sticky="s", padx=(50, 100))
        self.grid_count += 1

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.lb_title = []
        self.lb_body = []
        self.lb_body_callback = []
        self.out_text = tk.Text(background="black", fg="white")
        self.container = tk.Frame(self)
        self.title("Lab3")

        self._setup_grid(self.COLUMNS, self.ROWS)
        self._obj = DefaultMunch().fromDict(temp)
        self._update_params_grid()
        self._setup_log()
        self._update()
        self.mainloop()

    def _update(self):
        for callback in self.lb_body_callback:
            callback[0].set(callback[1]())
        self._log_insert(f"Packets Sent     | {self._obj.utils[0].body()}")
        self._log_insert(f"Packets Received | {self._obj.utils[1].body()}")
        # self._log_insert("Packets Received")
        self.after(1000, self._update)

    def _log_insert(self, msg: str):
        now = time.strftime("%H:%M:%S")
        self.out_text.config(state=NORMAL)
        self.out_text.insert(tk.END, f"[{now}]: {msg};\n")
        self.out_text.config(state=DISABLED)

    def _setup_log(self) -> None:
        self.out_text.grid(row=self.ROWS + 1, column=0, columnspan=self.COLUMNS, sticky="news", padx=(10, 10))

    def _update_params_grid(self):
        counter = 0
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                if counter >= len(self._obj.utils):
                    return
                self._print_div(self._obj.utils[counter].title, self._obj.utils[counter].body, row, col)
                counter += 1

    def _setup_grid(self, columns: int, rows: int, weight: int = 1) -> None:
        for column in range(columns):
            self.rowconfigure(index=column, weight=weight)

        for row in range(rows + 1):
            self.rowconfigure(index=row, weight=weight)


if __name__ == '__main__':
    main_win = Main()
    main_win.mainloop()
