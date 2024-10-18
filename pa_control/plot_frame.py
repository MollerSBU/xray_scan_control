import tkinter as tk
import numpy as np
import subprocess
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class plot_frame(tk.Frame):
    def __init__(self, parent, refresh_rate, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master = self)
        self.canvas.get_tk_widget().pack(fill = 'both', expand = True)

        self.refresh_rate = refresh_rate
        self.buffersize = 200

        self.ani = None
        self.data = []
        self.colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "brown", "white", "pink", "aqua", "xkcd:seafoam green"]
        

        self.__init_animation(refresh_rate)

    def __init_animation(self, refresh_rate):
        self.fig = plt.gcf()
        self.fig.set_size_inches(15, 6)
        self.ani = FuncAnimation(self.fig, self.__animate, interval=refresh_rate, blit=False)

    def __animate(self, i):
        self.__get_data()

        arr = np.array(self.data)
        arr = arr.T
        min = arr.min()
        max = arr.max()

        x = np.linspace(0, len(self.data), num = len(self.data))


        ax = plt.gca()
        ax.cla()
        ax.set_ylim([min, max])
        ax.set_ylabel("Current (nA)")
        ax.set_xlabel("Arb units (time)")
        ax.grid(visible = True, which = 'both')
        for j in range(12):
            ax.plot(x, arr[j], label = "Channel {}".format(j), color = self.colors[j])
        ax.set_facecolor('black')    
        ax.legend(loc="lower left")

    def __get_data(self):
        cmd = subprocess.run("echo currents | netcat -w 1 -t localhost 50001", 
        shell = True, executable = "/bin/bash",
        stdout = subprocess.PIPE, text=True)
    
        # clean data
        dat = cmd.stdout.strip("\n")
        dat = np.array([float(val.strip()) for val in dat.split(",")])
        dat = dat.tolist()
        self.data.append(dat)

        if(len(self.data) > self.buffersize):
            del self.data[0]