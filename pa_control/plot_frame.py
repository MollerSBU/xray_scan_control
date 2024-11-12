import tkinter as tk
from tkinter import messagebox
import numpy as np
import subprocess
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

'''
1. Gets data
2. Calls to update table
3. Handles plotting
'''


class plot_frame(tk.Frame):
    def __init__(self, parent, refresh_rate, table_frame, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master = self)
        self.canvas.get_tk_widget().pack(fill = 'both', expand = True)

        self.refresh_rate = refresh_rate

        # default buffersize
        self.buffersize = 200

        self.ani = None
        self.data = []
        self.colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "brown", "white", "pink", "aqua", "xkcd:seafoam green"]
        
        self.table_frame = table_frame

        self.__init_animation(refresh_rate)
        self.__initialize_widgets()

    # buttons work better with grid...
    # make seperate frame to contain entries/buttons/etc

    def __initialize_widgets(self):
        self.button_frame = tk.Frame(self)

        self.buffer_entry = tk.Entry(self.button_frame, text = "200", width = 10)
        tk.Label(self.button_frame, text = "Buffer Size: ").grid(row = 0, column = 0)
        tk.Button(self.button_frame, text = "Confirm", command = self.__confirm_buffersize).grid(row = 0, column = 2)
        tk.Button(self.button_frame, text = "Clear plot", command = self.__clear_data).grid(row = 0, column = 3)
        self.buffer_entry.grid(row = 0, column = 1)
        
        self.button_frame.pack(side = tk.LEFT, expand = "y")

    def __confirm_buffersize(self):
        try:
            self.buffersize = int(self.buffer_entry.get())
        except:
            messagebox.showerror(title = "Error", message = "Please enter an integer as buffersize")

    def __clear_data(self):
        del self.data[:-1]

    def __init_animation(self, refresh_rate):
        self.fig = plt.gcf()
        self.fig.set_size_inches(15, 6)
        self.ani = FuncAnimation(self.fig, self.__animate, interval=refresh_rate, blit=False, cache_frame_data= False)

    # main loop, refreshes using matplotlib ui instead of tkinter

    def __animate(self, i):
        
        # gets data
        self.__get_data()

        # updates table
        self.table_frame.update_table(self.data)

        arr = np.array(self.data)
        arr = arr.T
        min = arr.min()
        max = arr.max()

        x = np.linspace(0, len(self.data), num = len(self.data))

        ax = plt.gca()
        # clear previous axis
        ax.cla()
        # beautification
        ax.set_ylim([min, max])
        ax.set_ylabel("Current (nA)")
        ax.set_xlabel("Arb units (time)")
        ax.grid(visible = True, which = 'both')
        for j in range(12):
            ax.plot(x, arr[j], label = "Channel {}".format(j), color = self.colors[j])
        ax.set_facecolor('black')    
        ax.legend(loc="lower left")

    def __get_data(self):

        # gets data from command line
        cmd = subprocess.run("echo currents | netcat -w 1 -t localhost 50001", 
            shell = True, executable = "/bin/bash",
            stdout = subprocess.PIPE, text=True)
    
        # clean data
        dat = cmd.stdout.strip("\n")
        dat = np.array([float(val.strip()) for val in dat.split(",")])
        dat = dat.tolist()
        self.data.append(dat)

        # removes data (FIFO) until array length = that of bufersize
        if(len(self.data) > self.buffersize):
            del self.data[0:len(self.data) - self.buffersize]