import tkinter as tk
from .plot_frame import plot_frame
from .table_frame import table_frame

class pa_frame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.table_frame = table_frame(self)

        self.plot_frame = plot_frame(self, refresh_rate = 200, table_frame = self.table_frame)

        #self.plot_frame.grid(row = 0, column = 0, columnspan = 2)
        #self.table_frame.grid(row = 1, column = 0)
        self.plot_frame.pack(fill = 'x', expand = True, side = tk.TOP)
        self.table_frame.pack(fill = 'x', expand = True, side = tk.BOTTOM)

    def __initialize_widgets(self):
        pass
        # tk.Button(self, text = "Start Logging", command = self.__log_on)
        # tk.Button(self, text = "Stop Logging", command = self.__log_off)
        # self.log_status = tk.Label(self, text = "Logging: False")

        # self.table_buttons = []

        # for i in range(12):
        #     tk.Label(self, text = "Chan {}".format(i), width = 7).grid(row = 0, column = i+1)
        # for i in range(3):
        #     a = []
        #     for j in range(13):
        #         if j == 0:
        #             a.append(tk.Label(self, text="", width = 7))
        #         else:
        #             a.append(tk.Label(self, text="", borderwidth=1, relief="solid", width = 7))
        #         a[j].config(font=("TkDefaultFont", 17))
        #         #a[j].grid(row=i + 1, column=j)
        #     self.tablebuttons.append(a)
