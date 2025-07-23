import tkinter as tk
from tkinter import messagebox


'''
This is the input frame

This handles all user input, which can then be read in the output frame

This gets inputs for desired flow from user
'''

class input_frame(tk.Frame):
    # constructor
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.flow_rate = 1
        self.ratio = None

        self.flow_input = None
        self.mixture_input = None

        self.flag_new_setpoint = False

        self.__initialize_widgets()

    # initializes a few labels, and entry boxes for ratio/flow
    def __initialize_widgets(self):
        tk.Label(self, text = "Desired Flow (scc/m)", width = 20).grid(row = 0, column = 0)
        tk.Label(self, text = "Desired Ar Ratio", width = 20).grid(row = 1, column = 0)

        self.flow_input = tk.Entry(self, width = 12)
        self.flow_input.grid(row = 0, column = 1)

        self.mixture_input = tk.Entry(self, width = 12)
        self.mixture_input.grid(row = 1, column = 1)

        self.flow_label = tk.Label(self, text = "Set Flow    : {}".format(0), width = 20)
        self.flow_label.grid(row = 0, column = 2)
        self.ratio_label = tk.Label(self, text = "Set Mixture : {}".format("N/A"), width = 20)
        self.ratio_label.grid(row = 1, column = 2)


        tk.Button(self, text = "Enter", command = self.__setFlow).grid(row = 2, column = 1)
        self.warning_message = tk.Label(self, text = "No Warnings", width = 30, fg = 'black', bg = 'white')
        self.warning_message.grid(row = 3, column = 0)

        self.set_mfcs_to_zero = tk.BooleanVar(self, False)
        tk.Checkbutton(self, text = "Zero MFC on close?", variable = self.set_mfcs_to_zero, onvalue = True, offvalue = False).grid(row = 3, column = 2)


    # reads in the flow rate and argon ratio from user
    # goodness checking is done here
        
    def __setFlow(self):
        try:
            flow_rate_input = int(self.flow_input.get())
            ratio_input = float(self.mixture_input.get())

            # will not try and set flow rate > 500, < 0 or ar ratio less than 0 or greater than 1
            # yes/no box will display if argon ratio is set greater than 80%
            if ratio_input > 1 or ratio_input < 0:
                messagebox.showerror(message = "Invalid ratio! Enter Ar ratio 0 < r < 1")
                return
            elif ratio_input >= 0.8:
                if not messagebox.askyesno(message = "Argon ratio >= 80%, are you sure?"):
                    return
            if flow_rate_input > 2000 or flow_rate_input < 0:
                messagebox.showerror(message = "Invalid flow rate! Enter flow rate 0 < f < 500")
                return
            self.flow_rate = flow_rate_input
            self.ratio = ratio_input
            self.flow_label.config(text = "Set Flow    : {}".format(self.flow_rate))
            self.ratio_label.config(text = "Set Mixture : {}".format(self.ratio))
            # every refresh cycle, output frame checks truth of flag_new_setpoint
            # if true: it sets new values
            # if false: it reads current values
            self.flag_new_setpoint = True
        # all non-ints or floats for flow rate and ratio respectively should be caught by exception
        except:
            print("Invalide flow rate and/or Ar ratio")