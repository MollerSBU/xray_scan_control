import tkinter as tk
import os
from input_frame import input_frame
from output_frame import output_frame

'''
Handles all high level interaction with input/output frames

Generates input/output frames
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

if __name__ == "__main__":
    addresses = ["/dev/serial/by-id/usb-FTDI_USB-RS232_Cable_AU05T0I2-if00-port0", "/dev/serial/by-id/usb-FTDI_USB-RS232_Cable_AU05STIP-if00-port0"]
    addresses = [os.path.realpath(x) for x in addresses]
    root = tk.Tk()
    main_frame = mfc_GUI(root, addresses, 500)
    main_frame.pack()
    root.mainloop()