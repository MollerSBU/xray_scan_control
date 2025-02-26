import tkinter as tk
import threading
import queue
import alicat
import asyncio
import time

'''
This is the output frame

This does all interactions with mfc including:

1. Getting values from mfcs and displaying them
2. Writing setpoints to mfcs
3. Setting mfcs to 0 upon closing
'''

# get and set have similar functionalities, but get has to put returned values in queue
# to be read by other thread
# set returns None and does not need to be put in queue

def async_wrapper_get(mfc, queue):
    queue.put(asyncio.run(get_from_mfc(mfc)))

def async_wrapper_set(mfc, value):
    asyncio.run(set_to_mfc(mfc, value))

async def get_from_mfc(mfc):
    return await mfc.get()

async def set_to_mfc(mfc, value):
    await mfc.set_flow_rate(value)


class output_frame(tk.Frame):
    # constructor
    def __init__(self, parent, addresses, in_frame, refresh_rate, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # initializes input variables
        self.root = parent
        self.addresses = addresses
        self.in_frame = in_frame
        self.refresh_rate = refresh_rate

        self.threads = []


        # initializes variables
        # not strictly necessary, could be initialized in place
        self.row_labels = ["pressure", "temperature", "volumetric_flow", "mass_flow", "setpoint", "gas"]
        self.flow_labels = []
        self.out_dict = [None, None]
        self.mfc = [None, None]
        self.queue = [None, None]
        self.Ar_rate = 0
        self.CO2_rate = 0
        self.warning_enabled = False
        self.warning_counter = 0

        # henceforth mfc '0' is for Ar and mfc '1' is for CO2, could change
        asyncio.run(self.__init__mfc(self.addresses[0], 0))
        asyncio.run(self.__init__mfc(self.addresses[1], 1))

        self.__initialize_widgets()

        self.__main_refresher()


    # intializes the table of values 
    # for monitoring the mfcs
    def __initialize_widgets(self):
        N_mfc = 2
        N_rows = len(self.row_labels)
        tk.Label(self, text = "Gas Control").grid(row = 0, column = 0)
        tk.Label(self, text = "MFC 1", width = 8, font=("tkDefaultFont", 15)).grid(row = 1, column = 1)
        tk.Label(self, text = "MFC 2", width = 8, font=("tkDefaultFont", 15)).grid(row = 1, column = 2)
        for i in range(N_rows):
            tk.Label(self, text = self.row_labels[i], width = 15, font=("tkDefaultFont", 15)).grid(row = i+2, column = 0)
        for i in range(N_mfc):
            column = []
            for j in range(N_rows):
                column.append(tk.Label(self, text="", 
                                           borderwidth=1, 
                                           relief="solid", 
                                           width = 7,
                                           font=("tkDefaultFont", 15)))
                column[j].grid(row = j+2, column = i+1)
            self.flow_labels.append(column)

    # main refresher loop, every refresh rate, it check if new values have been entered,
    # if so: change them
    # if not: get values from mfcs
    # then do it again refresh_rate ms
    def __main_refresher(self):
        self.__check_threads()
        if self.in_frame.flag_new_setpoint:
            self.__set_values()
        else:
            self.__check_rate()
            if self.warning_enabled:
                self.__run_warning()
            self.__open_thread_get(0)
            self.__open_thread_get(1)
        self.root.after(self.refresh_rate, self.__main_refresher)

    def __check_threads(self):
        thread_alive = []
        for thread in self.threads:
            thread_alive.append(thread.is_alive())
        self.threads = [thread for thread in self.threads if thread_alive[self.threads.index(thread)]]

    # intializes the MFC based on USB address
    async def __init__mfc(self, address, n_mfc):
        self.mfc[n_mfc] = alicat.FlowController(address)
        gas = "Ar" if n_mfc == 0 else "CO2"
        await self.mfc[n_mfc].set_gas(gas)


    def __run_warning(self):
        self.warning_counter += 1
        self.__flash(self.in_frame.warning_message)
        self.in_frame.warning_message.configure(text = "WARNING: FLOW RATE \n DEVIATES FROM SET BY > 5%\n {} CYCLES UNTIL SHUTOFF".format(60 - self.warning_counter))
        # set argon flow to 0 if warning persists for 60 cycles of refresh rate (default is 2 Hz)
        if self.warning_counter >= 60:
            self.threads.append(threading.Thread(target = async_wrapper_set, args = (self.mfc[0], 0)))
            self.threads[-1].start()
            self.threads.append(threading.Thread(target = async_wrapper_set, args = (self.mfc[1], 0)))
            self.threads[-1].start()
            self.Ar_rate, self.CO2_rate = 0, 0
            self.__clear_warnings()
            self.in_frame.warning_message.configure(text = "GAS WAS SHUTOFF\nRATIO DEVIATED > 5%\n FOR > 60 CYCLES")

    # starts a new thread to run asyncio function
    # opens a new queue which is passed to the new thread so that values may be passed between threads 
    def __open_thread_get(self, n_mfc):
        self.queue[n_mfc] = queue.Queue()
        self.threads.append(threading.Thread(target = async_wrapper_get, args = (self.mfc[n_mfc], self.queue[n_mfc])))
        self.threads[-1].start()
        self.root.after(100, self.__process_queue, n_mfc)

    # checks every 100 ms if something has been added to queue
    def __process_queue(self, n_mfc):
        try:
            self.out_dict[n_mfc] = self.queue[n_mfc].get_nowait()
            if type(self.out_dict[n_mfc]) is dict:
                self.__set_table(self.out_dict[n_mfc], n_mfc)
        except queue.Empty:
            self.root.after(100, self.__process_queue, n_mfc)

    # sets mfc output in table
    def __set_table(self, vals, n_mfc):
        for i in range(len(self.row_labels)):
            self.flow_labels[n_mfc][i].config(text = vals[self.row_labels[i]])

    # if flag_new_setpoint is changed to True (in input_frame.py)
    # then we set new values to flow meters and change flag to false
    def __set_values(self):
        total_rate = self.in_frame.flow_rate
        ratio = self.in_frame.ratio
        self.Ar_rate = ratio * total_rate
        self.CO2_rate = (1 - ratio)* total_rate
        self.in_frame.flag_new_setpoint = False
        self.threads.append(threading.Thread(target = async_wrapper_set, args = (self.mfc[0], self.Ar_rate)))
        self.threads[-1].start()
        self.threads.append(threading.Thread(target = async_wrapper_set, args = (self.mfc[1], self.CO2_rate)))
        self.threads[-1].start()

    def __check_rate(self):
        if self.out_dict[0] is not None and self.Ar_rate != 0 and self.CO2_rate != 0:
            flag = False
            for i in range(2):
                correct_rate = self.Ar_rate if i == 0 else self.CO2_rate
                current_flow = self.out_dict[i]['mass_flow']
                if current_flow < correct_rate * 0.95 or current_flow > correct_rate * 1.05:
                    flag = True
            if flag and not self.warning_enabled:
                self.in_frame.warning_message.config(text = "WARNING: FLOW RATE \n DEVIATES FROM SET BY > 5%", fg = "red", bg = 'white')
                self.warning_enabled = True
            elif not flag and self.warning_enabled:
                self.__clear_warnings()

    def __flash(self, label):
        if self.warning_enabled:
            bg = label.cget("background")
            fg = label.cget("foreground")
            label.configure(background=fg, foreground=bg)
            self.configure(background = fg)

    # behavior upon closing window
    # set both mfcs to 0 flow and then destroy root
    def on_closing(self):
        self.__check_threads()
        while len(self.threads) != 0:
            print("Waiting for {} threads to close".format(len(self.threads)))
            self.__check_threads()
            if len(self.threads) != 0:
                time.sleep(1)
        if self.in_frame.set_mfcs_to_zero.get():
            self.__clear_warnings()
            for i in range(2):
                self.__closing_wrapper(i)
            
    def __closing_wrapper(self, n_mfc):
        self.threads.append(threading.Thread(target = async_wrapper_set, args = (self.mfc[n_mfc], 0)))
        self.threads[-1].start()

    def __clear_warnings(self):
        self.configure(background = "#d9d9d9")
        self.in_frame.warning_message.config(text = "No Warnings", fg = 'black', bg = 'white')
        self.warning_enabled = False
        self.warning_counter = 0
