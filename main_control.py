import tkinter as tk
import gas_control.mfc_gui_async
import xray_control.xray_frame
import pa_control.pa_frame
import motor_control.motor_frame
from tkinter import messagebox

#

class main_frame:
    def __init__(self, parent):
        self.root = parent
        
        self.__initialize_mfc_gui()
        self.__iniitialize_xray_gui()
        self.__initialize_pa_gui()
        self.__intialize_motor_gui()

        self.root.protocol("WM_DELETE_WINDOW", self.__close_safely)

    def __initialize_mfc_gui(self):
        addresses = ["/dev/ttyUSB1", "/dev/ttyUSB0"]
        self.gas_frame = gas_control.mfc_gui_async.mfc_GUI(self.root, 
                addresses, refresh_rate = 500, borderwidth=3, relief=tk.RIDGE)
        #self.gas_frame.pack(fill='both', side = tk.RIGHT, expand = True)
        self.gas_frame.grid(row = 0, column = 1, stick = "nsw")
    def __iniitialize_xray_gui(self):
        self.xray_frame = xray_control.xray_frame.xray_frame(self.root, 
                refresh_rate = 500, borderwidth=3, relief=tk.RIDGE)
        #self.xray_frame.pack(fill = 'both', side = tk.LEFT, expand = False)
        self.xray_frame.grid(row = 0, column = 0)

    def __initialize_pa_gui(self):
        self.pa_frame = pa_control.pa_frame.pa_frame(self.root, 
                borderwidth = 3, relief = tk.RIDGE)
        #self.pa_frame.pack(fill='both', side = tk.BOTTOM, expand = True)
        self.pa_frame.grid(row = 1, column = 0, columnspan = 3, sticky = "sw")

    def __intialize_motor_gui(self):
        self.motor_frame = motor_control.motor_frame.motor_frame(self.root,
                borderwidth = 3, relief = tk.RIDGE)
        self.motor_frame.grid(row = 0, column = 2, sticky = "nw")

    def __close_safely(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.gas_frame.out_frame.on_closing()
            self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    main_frame = main_frame(root)
    root.mainloop()