import tkinter as tk
import os

class image_frame(tk.Frame):
    def __init__(self, parent, refresh_rate, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.__refresh_rate = refresh_rate
        self.__plot = None
        self.__image_path = "/home/mollergem/MOLLER_xray_gui/scan_control/.tmp/test.gif"

        self.__initialize_widgets()
        self.__main_refresher()


    def __initialize_widgets(self):
        self.__display_plot = tk.BooleanVar(self, False)
        tk.Checkbutton(self, text = "Display plot ", variable = self.__display_plot, onvalue = True, offvalue = False).pack(side = tk.TOP)
        self.__image_label = tk.Label(self)

    def __main_refresher(self):
        if os.path.exists(self.__image_path):
            self.__plot = tk.PhotoImage(file = self.__image_path)
        
        if self.__plot is not None and self.__display_plot.get():
            self.__image_label.configure(image = self.__plot)
        else:
            self.__image_label.configure(image = None)
        self.__image_label.pack(side = tk.LEFT, expand = True)

        self.after(self.__refresh_rate, self.__main_refresher)

            