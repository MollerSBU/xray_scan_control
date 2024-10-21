import tkinter as tk
import subprocess
from tkinter import messagebox, simpledialog
import os
from threading import Thread


def run_scan(voltage, directory):
    subprocess.run("/home/mollergem/MOLLER_xray_gui/scan_control/scanscripts/gainScan.sh {} {}".format(voltage, directory), 
                       shell=True, stdout = subprocess.PIPE)

class scan_frame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__initialize_widgets()

    def __initialize_widgets(self):
        tk.Label(self, text = "Scan control").grid(row = 0, column = 0)
        tk.Label(self, text = "Directory:").grid(row = 1, column = 0)
        self.directory_name = tk.Entry(self)
        self.directory_name.grid(row = 1, column = 1)
        tk.Button(self, text = "Confirm", command = self.__check_directory).grid(row = 1, column = 2)
        #self.status = tk.Label(self, text = "Status: Unknown")
        #self.status.grid(row = 2, column = 0)
        self.directory = None

        run_select = {"voltage": "voltage", "position": "position"}
        self.run_type = tk.StringVar(self, "voltage")

        i = 0
        for (text, value) in run_select.items():
            tk.Radiobutton(self, text = text,
                            variable = self.run_type,
                            value = value).grid(row = 2, column = i)
            i += 1

        tk.Button(self, text = "Begin Run", command = self.__confirm_run).grid(row = 4, column = 0)

    def __confirm_run(self):
        if messagebox.askokcancel("Begin Scan", "About to begin scan, are you sure?"):
            if self.run_type.get() == "voltage":
                self.__run_voltage_scan()
            elif self.run_type.get() == "position":
                self.__run_position_scan()

    def __run_voltage_scan(self):
        if self.directory is None:
            messagebox.showerror(title = "Directory Error",
                    message = "Please enter a directory first")
            return
        inp = simpledialog.askinteger(title = "Voltage",
                    prompt = "Enter intended voltage")
        while not messagebox.askokcancel(title = "Confirm", 
                message = "You have entered {}, confirm?".format(inp)):
            inp = inp = simpledialog.askinteger(title = "Voltage",
                        prompt = "Enter intended voltage")
            if inp is None:
                return

        #self.status.config(text = "Status: Voltage Scan Running")
        
        thread = Thread(target = run_scan, args = (inp, self.directory))
        thread.start()

    def __run_position_scan(self):
        messagebox.showwarning(title = "Not Implemented",
            message = "Position scan is not yet implemented")

    def __check_directory(self):
        dirname = self.directory_name.get()
        if any(not char.isalnum() for char in dirname):
            messagebox.showerror(title = "Invalid Directory", 
                message = "Invalid directory, please use only letters and numbers")
            return
        if not os.path.isdir("/home/mollergem/MOLLER_xray_gui/scans/{}".format(dirname)):
            os.mkdir("/home/mollergem/MOLLER_xray_gui/scans/{}".format(dirname))

        self.directory = "/home/mollergem/MOLLER_xray_gui/scans/{}".format(dirname)