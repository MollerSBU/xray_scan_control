import tkinter as tk
import subprocess
from tkinter import messagebox

class motor_frame(tk.Frame):
    def __init__(self, parent, motorport, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__motorport = motorport
        self.__initialize_widgets()

    def __initialize_widgets(self):
        tk.Label(self, text = "Motor Position Control").grid(row = 0, column = 0, columnspan = 3)
        tk.Button(self, text = "Init", command = self.__init_motor, width = 7).grid(row = 1, column = 0, sticky = "w")
        tk.Button(self, text = "Halt", command = self.__halt, width = 7).grid(row = 1, column = 1, stick = "w")
        tk.Button(self, text = "Move", command = self.__controlled_move, width = 7).grid(row = 2, column = 0, stick = "w")
        
        tk.Label(self, text = "Target: ").grid(row = 2, column = 1)
        self.con_move_position = tk.Entry(self, width = 7)
        self.con_move_position.insert(tk.END, 5000)
        self.con_move_position.grid(row = 2, column = 2)

        motor_target_dict = {"x": 3, "y": 1}
        self.motor_selection = tk.IntVar(self, 3)
        i = 3
        for (text, value) in motor_target_dict.items():
            tk.Radiobutton(self, text = text, 
                           variable = self.motor_selection, 
                           value = value).grid(row = 2, column = i)
            i += 1
        

    def __init_motor(self):
        subprocess.run("~/MOLLER_xray_gui/motor_control/motorscripts/newmotorinit.sh {}".format(self.__motorport),
                        shell=True, executable = "/usr/bin/bash", stdout = subprocess.PIPE, text = True)

    def __controlled_move(self):
        pos = int(self.con_move_position.get())
        motor = self.motor_selection.get()
        subprocess.run("~/MOLLER_xray_gui/motor_control/motorscripts/controlledmove.sh {} {} {}".format(pos, motor, self.__motorport),
                       shell=True, executable = "/usr/bin/bash", stdout = subprocess.PIPE)
        
    def __halt(self):
        if messagebox.askokcancel("Halt", "Are you sure you want to halt?"):
            subprocess.run("~/MOLLER_xray_gui/motor_control/motorscripts/HaltMeasurements.sh {}".format(self.__motorport),
                        shell=True, executable = "/usr/bin/bash", stdout = subprocess.PIPE, text = True)