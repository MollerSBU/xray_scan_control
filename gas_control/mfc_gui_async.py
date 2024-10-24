import tkinter as tk
from .input_frame import input_frame
from .output_frame import output_frame

'''
Handles all high level interaction with input/output frames

Generates input/output frames
Handles closing functionality
Initializes run
'''

class mfc_GUI(tk.Frame):
    def __init__(self, parent, address, refresh_rate, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent

        in_frame = input_frame(self)
        in_frame.pack(fill='both', side = tk.BOTTOM, expand = True)

        self.out_frame = output_frame(self, address, in_frame, refresh_rate)
        self.out_frame.pack(fill='both', side = tk.TOP, expand = True)



if __name__ == '__main__':
    root = tk.Tk()
    gui = mfc_GUI(root, ["/dev/ttyUSB1", "/dev/ttyUSB0"], 500)
    root.mainloop()