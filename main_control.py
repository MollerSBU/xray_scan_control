import tkinter as tk
import gas_control.mfc_gui_async
import xray_control.xray_frame
import pa_control.pa_frame
import motor_control.motor_frame
import scan_control.scan_frame
import scan_control.image_frame
from tkinter import messagebox
import os
import sys


class main_frame:
    def __init__(self, parent):
        self.root = parent
        
        self.__initialize_mfc_gui()
        self.__initialize_xray_gui()
        self.__initialize_pa_gui()
        self.__initialize_motor_gui()
        self.__initialize_scan_gui()
        self.__initialize_image_gui()

        self.root.protocol("WM_DELETE_WINDOW", self.__close_safely)



    def __initialize_mfc_gui(self):
        # /dev/serial/by-id contains serial devices listed with their unique ID
        # these have symlinks to the appropriate USB device
        # as long as cables are never swapped this should remain fine.
        addresses = ["/dev/serial/by-id/usb-FTDI_USB-RS232_Cable_AU05T0I2-if00-port0", "/dev/serial/by-id/usb-FTDI_USB-RS232_Cable_AU05STIP-if00-port0"]
        addresses = [os.path.realpath(x) for x in addresses]
        self.gas_frame = gas_control.mfc_gui_async.mfc_GUI(self.root, 
                addresses, refresh_rate = 500, borderwidth=3, relief=tk.RIDGE)
        #self.gas_frame.pack(fill='both', side = tk.RIGHT, expand = True)
        self.gas_frame.grid(row = 0, column = 1, stick = "nsw")
    def __initialize_xray_gui(self):
        self.xray_frame = xray_control.xray_frame.xray_frame(self.root, 
                refresh_rate = 500, borderwidth=3, relief=tk.RIDGE)
        #self.xray_frame.pack(fill = 'both', side = tk.LEFT, expand = False)
        self.xray_frame.grid(row = 0, column = 0)

    def __initialize_pa_gui(self):
        self.pa_frame = pa_control.pa_frame.pa_frame(self.root, 
                refresh_rate = 200, borderwidth = 3, relief = tk.RIDGE)
        #self.pa_frame.pack(fill='both', side = tk.BOTTOM, expand = True)
        self.pa_frame.grid(row = 1, column = 0, columnspan = 3, sticky = "sw")

    def __initialize_motor_gui(self):
        self.motor_frame = motor_control.motor_frame.motor_frame(self.root,
                borderwidth = 3, relief = tk.RIDGE)
        self.motor_frame.grid(row = 0, column = 2, sticky = "nw")

    def __initialize_scan_gui(self):
        self.scan_frame = scan_control.scan_frame.scan_frame(self.root,
                refresh_rate = 15000, borderwidth = 3, relief = tk.RIDGE)
        self.scan_frame.grid(row = 0, column = 3, sticky = "nw")

    def __initialize_image_gui(self):
        self.image_frame = scan_control.image_frame.image_frame(self.root,
                refresh_rate = 15000, borderwidth = 3, relief = tk.RIDGE)
        self.image_frame.grid(row = 1, column = 3, sticky = "sw")

    def __close_safely(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            # may need to turn gas off when frame is turned off
            # also, both of these frames use multithreading 
            self.gas_frame.out_frame.on_closing()
            self.scan_frame.on_closing()
            #self.root.destroy()
            sys.exit()

if __name__ == '__main__':
    root = tk.Tk()
    main_frame = main_frame(root)
    root.mainloop()