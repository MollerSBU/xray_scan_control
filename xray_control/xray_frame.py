import tkinter as tk
import subprocess
import numpy as np
from tkinter import messagebox

class xray_frame(tk.Frame):
    def __init__(self, parent, refresh_rate, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # In order array is
        # todo: explain all parameters
        self.refresh_rate = refresh_rate

        self.keys = ["LV", "cT", "kV", "mA", "fA", "fV", "hT", "HV", "IL", "FA"]
        self.current_values = {key: None for key in self.keys}
        self.__initialize_widgets()
        self.__main_refresher()
    
    def __main_refresher(self):
        self.__update_current_values()
        self.after(self.refresh_rate, self.__main_refresher)

    def __initialize_widgets(self):
        tk.Label(self, text = "X-Ray Generation").grid(row = 0, column = 0, padx = 3, pady = 3)
        tk.Button(self, text = "X-Rays: Init", command = self.__init_xray, width = 20).grid(row = 1, column = 0, columnspan = 3, padx = 3, pady = 3)
        tk.Button(self, text = "X-Rays: HV On", command = self.__hv_on, height = 3).grid(row = 2, column = 0, rowspan = 2, padx = 3, pady = 3)
        tk.Button(self, text = "X-Rays: HV Off", command = self.__hv_off, width = 20).grid(row = 4, column = 0, columnspan = 3, padx = 3, pady = 3)
        self.set_voltage = tk.Entry(self, width = 10)
        self.set_voltage.insert(tk.END, "15")
        self.set_current = tk.Entry(self, width = 10)
        self.set_current.insert(tk.END, "0.02")
        tk.Label(self, text = "kV").grid(row = 2, column = 2, padx = 3, pady = 3)
        tk.Label(self, text = "mA").grid(row = 3, column = 2, padx = 3, pady = 3)
        tk.Label(self, text = "Accel:").grid(row = 5, column = 0, padx = 3, pady = 3)
        tk.Label(self, text = "Current:").grid(row = 6, column = 0, padx = 3, pady = 3)
        tk.Label(self, text = "Filament:").grid(row = 7, column = 0, padx = 3, pady = 3)
        self.current_hv       = tk.Label(self, text = "{}".format(self.current_values["kV"]))
        self.current_current  = tk.Label(self, text = "{}".format(self.current_values["mA"]))
        self.current_filament = tk.Label(self, text = "{}".format(self.current_values["fA"]))
        self.hv_faults        = tk.Label(self, text = "Unknown", background = "red", width = 20)
        self.interlock_faults = tk.Label(self, text = "Unknown", background = "red", width = 20)
        self.faults           = tk.Label(self, text = "Unknown", background = "red", width = 20)

        self.set_voltage.grid(row = 2, column = 1, padx = 3, pady = 3)
        self.set_current.grid(row = 3, column = 1, padx = 3, pady = 3)
        self.current_hv.grid(row = 5, column = 2, padx = 3, pady = 3)   
        self.current_current.grid(row = 6, column = 2, padx = 3, pady = 3)
        self.current_filament.grid(row = 7, column = 2, padx = 3, pady = 3)
        self.hv_faults.grid(row = 8, column = 0, columnspan = 3, padx = 3, pady = 3)
        self.interlock_faults.grid(row = 9, column = 0, columnspan = 3, padx = 3, pady = 3)
        self.faults.grid(row = 10, column = 0, columnspan = 3, padx = 3, pady = 3)

    # intialize x-ray
    def __init_xray(self):
        if not bool(self.current_values["HV"]):
            subprocess.run("~/MOLLER_xray_gui/xray_control/xray_scripts/setup_xRayGun.sh", shell=True, executable = "/usr/bin/sh", stdout = subprocess.PIPE, text = True)
        else:
            messagebox.showerror("Error", "Don't initialize the X-Ray while the HV is on.")

    # read entries containg values to change to and then turn on hv
    def __hv_on(self):
        mA_to = int(float(self.set_current.get()) * 4095 / 5)
        kV_to = int(float(self.set_voltage.get()) * 4095 / 65)
        subprocess.run("~/MOLLER_xray_gui/xray_control/xray_scripts/xRayGun_ON.sh -k {} -m {}".format(kV_to, mA_to)
                       , shell=True, executable = "/usr/bin/sh", stdout = subprocess.PIPE, text = True)

    # turn hv off
    def __hv_off(self):
        subprocess.run("~/MOLLER_xray_gui/xray_control/xray_scripts/xRayGun_OFF.sh", shell=True, executable = "/usr/bin/sh", stdout = subprocess.PIPE, text = True)

    def __get_current_values(self):
        cmd_vals = subprocess.run("~/Products/XRay/xray_client_tcp 192.168.1.4 20, ", 
                             shell=True, stdout = subprocess.PIPE, text = True)
        # output looks like:
        # CompletedProcess(args='~/Products/XRay/xray_client_tcp 192.168.1.4 20, ', 
        #                  returncode=0, stdout='20,433,2276,1,1,228,88,334,\n')
        # we take the stdout, remove the newline, and split at commas
        # also have to remove trailing comma and we dont really care what command is run
        cmd_faults = subprocess.run("~/Products/XRay/xray_client_tcp 192.168.1.4 22, ", 
                             shell=True, stdout = subprocess.PIPE, text = True)

        cmd_response_vals = cmd_vals.stdout.strip("\n").split(",")[1:-1]
        cmd_response_faults = cmd_faults.stdout.strip("\n").split(",")[1:-1]
        vals = [int(val) for val in cmd_response_vals + cmd_response_faults]
        return vals

    def __update_current_values(self):
        try:
            vals = self.__get_current_values()
            self.current_values = dict(zip(self.keys, vals))

            self.current_values["kV"] = (self.current_values["kV"] * 65000 / 4096) / 1000
            self.current_values["mA"] = (self.current_values["mA"] * 6000 / 4096) / 1000
            self.current_values["fA"] = (self.current_values["fA"] * 1000 / 4096) / 100

            self.current_hv.config(text = "{:.2f} kV".format(round(self.current_values["kV"], 2)))
            self.current_current.config(text = "{:.3f} mA".format(round(self.current_values["mA"], 3)))
            self.current_filament.config(text = "{:.2f} fA".format(round(self.current_values["fA"], 2)))

            # HV = 0 if off, interlock = 0 if closed, faults = 0 if there are none

            if(bool(self.current_values["HV"])):
                self.hv_faults.config(text = "High Voltage:  ON", bg = "green")
            else:
                self.hv_faults.config(text = "High Voltage: OFF", bg = "red")

            if(not bool(self.current_values["IL"])):
                self.interlock_faults.config(text = "Interlocks: OK", bg = "green")
            else:
                self.interlock_faults.config(text = "Interlocks: OPEN", bg = "red")

            if(not bool(self.current_values["FA"])):
                self.faults.config(text = "No Faults", bg = "green")
            else:
                self.faults.config(text = "Fault Condition", bg = "red")
        except:
            self.current_hv.config(text = "ERR")
            self.current_current.config(text = "ERR")
            self.current_filament.config(text = "ERR")
            messagebox.showwarning("Warning", "Could not read parameters.\nPlease wait to see if issue fixes itself.\nIf not please restart.")


