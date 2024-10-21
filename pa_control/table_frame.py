import tkinter as tk
import numpy as np

class table_frame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__initialize_widgets()

    def __initialize_widgets(self):
        self.table_labels = []
        for i in range(12):
            tk.Label(self, text = "Chan {}".format(i), width = 7).grid(row = 0, column = i+1)
        for i in range(3):
            a = []
            for j in range(13):
                if j == 0:
                    a.append(tk.Label(self, text="", width = 7))
                else:
                    a.append(tk.Label(self, text="", borderwidth=1, relief="solid", width = 7))
                a[j].config(font=("TkDefaultFont", 13))
                a[j].grid(row=i + 1, column=j)
            self.table_labels.append(a)

    def update_table(self, data):
        data = np.array(data)
        run_length = 50 if len(data) > 50 else len(data)
        for i in range(13): #Columns
            for j in range(3): #Rows
                name = ""
                # Column 0 is variable name
                if i == 0:
                    if j == 0:
                        name = "Cur (nA)"
                    elif j == 1:
                        name = "Std"
                    else:
                        name = "μ {}".format(run_length)
                else:
                    if j == 0:
                        name = round(data.T[i-1][-1], 3)
                    elif j == 1:
                        name = round(np.std(data.T[i-1]),3)
                    else:
                        name = round(np.average(data.T[i-1][-run_length:]),3)
                self.table_labels[j][i].config(text = name)