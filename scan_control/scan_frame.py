import tkinter as tk
import subprocess
from tkinter import messagebox, simpledialog
import os
import threading
import multiprocessing
import time
from .generate_plot import generate_plot


def run_voltage_scan(voltage, directory, motorport):
    subprocess.run("/home/mollergem/MOLLER_xray_gui/scan_control/scanscripts/gainScan.sh {} {} {}".format(voltage, directory, motorport), 
                       shell=True, stdout = subprocess.PIPE)

def run_long_position_scan(fname, directory, motorport):
    subprocess.run("/home/mollergem/MOLLER_xray_gui/scan_control/scanscripts/mollerScan_alpha.sh {} {} {}".format(fname, directory, motorport), 
                      shell=True, stdout = subprocess.PIPE)

def run_cont_position_scan(fname, directory, motorport):
    subprocess.run("/home/mollergem/MOLLER_xray_gui/scan_control/scanscripts/moller_scan_continuous.sh {} {} {}".format(fname, directory, motorport), 
                      shell=True, stdout = subprocess.PIPE)

def plot(directory, fname, continuous_scan):
    if not continuous_scan:
        generate_plot(directory, fname)


class scan_frame(tk.Frame):
    def __init__(self, parent, refresh_rate, motorport, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__directory = None
        self.__position_fname = None
        self.__refresh_rate = refresh_rate
        self.__position_scan_running  = False
        self.__motorport = motorport

        self.__continuous_scan = True

        self.plot_thread, self.position_scan_thread, self.voltage_scan_thread = None, None, None
        self.__initialize_widgets()
        self.__main_refresher()


    def __main_refresher(self):
        if self.__position_scan_running and os.path.exists("{}/{}".format(self.__directory, self.__position_fname)):
            get_plot = True
            last_write = os.path.getmtime("{}/{}".format(self.__directory, self.__position_fname))
            time_since_last_write = time.time() - last_write
            if time_since_last_write > 60:
                if messagebox.askokcancel(title = "ERROR", message = "Scan file hasn't updated in more than 60 seconds, please check if motor is still running. Press 'OK' if everything is fine, and 'CANCEL' if not."):
                    pass
                else:
                    self.__position_scan_running = False
                    get_plot = False
            if get_plot:
                self.plot_thread = multiprocessing.Process(target = plot, args = (self.__directory, self.__position_fname, self.__continuous_scan))
                self.plot_thread.start()
        self.after(self.__refresh_rate, self.__main_refresher)

    def __initialize_widgets(self):
        tk.Label(self, text = "Scan control").grid(row = 0, column = 0)
        tk.Label(self, text = "Directory:").grid(row = 1, column = 0)
        self.__directory_name = tk.Entry(self)
        self.__directory_name.grid(row = 1, column = 1)
        tk.Button(self, text = "Confirm", command = self.__check_directory).grid(row = 1, column = 2)
        #self.status = tk.Label(self, text = "Status: Unknown")
        #self.status.grid(row = 2, column = 0)

        run_select = {"voltage": "voltage", "position_long": "position long", "position_cont": "position cont"}
        run_select = {"voltage": "voltage", "position_long": "position long", "position_cont": "position cont"}
        self.__run_type = tk.StringVar(self, "voltage")

        i = 0
        for (text, value) in run_select.items():
            tk.Radiobutton(self, text = text,
                            variable = self.__run_type,
                            value = value).grid(row = 2, column = i)
            i += 1

        tk.Button(self, text = "Begin Run", command = self.__confirm_run).grid(row = 4, column = 0)

    def __confirm_run(self):
        if messagebox.askokcancel("Begin Scan", "About to begin scan, are you sure?"):
            if self.__run_type.get() == "voltage":
                self.__run_voltage_scan()
            elif self.__run_type.get() == "position_long":
                self.__run_long_position_scan()
            elif self.__run_type.get() == "position_cont":
                self.__run_cont_position_scan()

    def __run_voltage_scan(self):
        if not self.__valid_directory():
            return
        inp = simpledialog.askinteger(title = "Voltage",
                    prompt = "Enter intended voltage")
        while not messagebox.askokcancel(title = "Confirm", 
                message = "You have entered {}, confirm?".format(inp)):
            inp = simpledialog.askinteger(title = "Voltage",
                        prompt = "Enter intended voltage")
            if inp is None:
                return
        
        self.voltage_scan_thread = multiprocessing.Process(target = run_voltage_scan, args = (inp, self.__directory, self.__motorport))
        self.voltage_scan_thread.start()

    def __run_long_position_scan(self):
        if not self.__valid_directory():
            return
        if not messagebox.askokcancel(title = "Confirm",
                message = "Are you sure you want to initiate a position scan? It cannot be easily stopped once started."):
            return
        self.__continuous_scan = False
        self.__position_fname = time.strftime("%Y-%m-%d_%H:%M", time.gmtime())
        self.__position_scan_running = True
        self.position_scan_thread = multiprocessing.Process(target = run_long_position_scan, args = (self.__position_fname, self.__directory, self.__motorport))
        self.position_scan_thread.start()
    
    def __run_cont_position_scan(self):
        if not self.__valid_directory():
            return
        if not messagebox.askokcancel(title = "Confirm",
                message = "Are you sure you want to initiate a position scan? It cannot be easily stopped once started."):
            return
        self.__position_fname = time.strftime("%Y-%m-%d_%H:%M", time.gmtime())
        self.__position_scan_running = True
        self.position_scan_thread = multiprocessing.Process(target = run_cont_position_scan, args = (self.__position_fname, self.__directory, self.__motorport))
        self.position_scan_thread.start()

    def __check_directory(self):
        dirname = self.__directory_name.get()
        if any(not char.isalnum() for char in dirname):
            messagebox.showerror(title = "Invalid Directory", 
                message = "Invalid directory, please use only letters and numbers")
            return
        if not os.path.isdir("/home/mollergem/MOLLER_xray_gui/scans/{}".format(dirname)):
            os.mkdir("/home/mollergem/MOLLER_xray_gui/scans/{}".format(dirname))

        self.__directory = "/home/mollergem/MOLLER_xray_gui/scans/{}".format(dirname)

    def __valid_directory(self):
        if self.__directory is None:
            messagebox.showerror(title = "Directory Error",
                    message = "Please enter a directory first")
            return False
        return True
    
    def on_closing(self):
        if self.plot_thread is not None:
            self.plot_thread.terminate()
        if self.position_scan_thread is not None:
            self.position_scan_thread.terminate()
        if self.voltage_scan_thread is not None:
            self.voltage_scan_thread.terminate()