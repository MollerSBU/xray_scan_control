import tkinter as tk
from .plot_frame import plot_frame
from .table_frame import table_frame

'''
Master frame that initializes two subframes

One controlling the table

One controlling the plot
'''

class pa_frame(tk.Frame):
    def __init__(self, parent, refresh_rate, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.table_frame = table_frame(self)

        self.plot_frame = plot_frame(self, refresh_rate = refresh_rate, table_frame = self.table_frame)

        #self.plot_frame.grid(row = 0, column = 0, columnspan = 2)
        #self.table_frame.grid(row = 1, column = 0)
        self.plot_frame.pack(fill = 'x', expand = True, side = tk.TOP)
        self.table_frame.pack(fill = 'x', expand = True, side = tk.BOTTOM)