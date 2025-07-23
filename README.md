# MOLLER X-Ray scan control

To run

```
python3 main_control.py
```

## Explanation of control

This section will go over each frame and what every control does


If any frame needs to be disabled for any reason, simply go into main_control.py and comment out the respective frame on line 22-27. I also have some slightly outdate code for the gas control inside of ./standalone_gas that will bring up just the gas frame with nothing else. One could also for example comment out every other frame but the gas control.

## X-Ray Frame

This section control the x-ray. The x-ray communicates over tcp and will work as long as it's on the same network as the computer.

While ramping up the detector to voltage, HV should be OFF. Prior to turning on the X-Ray for the first time, press "X-Rays: Init".

The default values for the voltage and current should not be deviated from except under special circumstances

After a scan is run, the X-Ray should turn off automatially. In the case of a position dependent gain scan, the motor may stall during the test. In this case, turn the X-ray off as soon as this issue is noticed.

### How it works

The code is stored in ./xray_control/xray_frame.py, which runs scripts in ./xray_control/xray_scripts/. The main x-ray control code and server is all in ~/Products/XRay

There is a little bit of documentation inside the above directory for how the commands inside the scripts actually work. Example of how to turn on the X-Ray (only after initialzation is shown below)

        ~/MOLLER_xray_gui/xray_control/xray_scripts/xRayGun_ON.sh -k {} -m {}

-k is to set the voltage, -m the current. Replace curly braces with the values, dont use the curly braces. You have to set them in ADC values, not in real values and the conversion is done as such:

floor(I \* 4095 / 5), where I is in mA
floor(V \* 4095 / 65), where V is in kV

This conversion is already done inside the GUI (Lines 61-62 inside xray_frame.py)

The setup (i.e., X-Rays: Init button) must be pressed after every time the X-Ray system is turned on and just runs the script "setup_xRayGun.sh"


### Some problems and solutions

1. The door/interlock is closed but the frame is still showing interlock as open

        Press the green button on the X-Ray control bin

2. When opening the main control, errors come up about not being able to communicate with the x-ray

        Ensure that the internet cord is plugged in. Try pinging 192.168.1.4. This is the IP of the X-Ray, if it doesn't ping something is amiss.


## Gas Control Frame

This frame allows for control and monitoring of the gas mixing unit. 

The most import thing to watch for are that no errors (bottom left) pop up. The frame will flash red and an error will pop up in the bottom left. This happens if gas flow deviates from what is set by more than 5%.

The control of the flow rate and mixing ratio should mostly remain constnat. Ensure that argon is flowing at ratio \* flow_rate and co2 is flowng at (1-ratio)
\* flow_rate. Mass flow is the important quantity, not volumetric flow.

### How it works

The main code is stored in ./gas_control. I tried to comment the lines of this code but will do a high level overview here. The code is all controlled at the most basic level through the alicat package, of which documentation can be found by typing "alicat -h". There is also a python interface which is what's used in the code. 

To put it simply, each MFC is an object, and we use the methods of this object to control the flow rate. All of the python interface is written using the "asyncio" package which is written to allow native parallel processing when running the commands.

The "input_frame.py" controls all user input and logic. I.e., getting desired flow rate and checking for some warnings. Most of the code is inside "output_fame.py" which controls all I/O with the mfcs themselves. The function "__main_refresher" is what actually runs most of the code. Based on a desired refresh rate, it checks for new user input, or if something is a problem with the flow. The default refresh rate is 500 ms.

When new values are input, it starts a new thread to set these values to the MFC, and waits around until it's happened. It does this through data structures called "queues" which are only used because of the multithreading aspect. 

MFCS are initialized by USB address, which I set based on the USB address of the cord. If the code is changed for any reason, this has to be updated in mfc_gui_async.py. As long as the same cords are used this isn't an issue.

### Some issues

1. One important thing I discovered is that for the LPM MFC, the alicat code has a bug where it truncates whatever values is input to it to only two decimal places (despite the MFC itself being capable of handling 4 decimal places) I wrote code (lines 195-205 of output_frame.py) to automatically take the user input and find the closest two decimal point flow for the LPM. There is also a long writeup there to explain the logic

## Motor Control frame

Will briefly explain how the motors work here too. The motors are controlled in "motor units" which correspond to 5 um each (i.e., 2000 motor units is 1 cm). The X motor is the master and the Y motor is the slave. The motors can handle diagonal movement at once if given to them. There is an example motor script in ./scan_control/scanscripts/example_script.sh with lots of comments to give an example of how to make a script that covers the area of a given detector.

This frame is rarely used. Sometimes if the motor has not been used in a while or has been unplugged, movement will not work. One can try doing a small movement in x and y to ensure the motor is responsive. The halt button will not work 9 times out of 10. There is no real way to get it to work. You dont have to initialize a new motor before each scan. The scans will do this automatically when run.

It is not written parallely, so it will make the rest of the GUI freeze when used. 

### Some problems and solutions

1. The motor is unresponsive and doesnt move when given position and command

        First just make sure that you arent trying to move it to somewhere it already is. If it's not, try moving the motor manually using the buttons on the controller. That is, on the VXM stepping motor controller, press the buttons on each controller that say "Jog 1", in each direction.

## Scan Frame

This controls two things

1. It handles running scripts (which are stored in ./scan_control/scanscripts)
2. It does some plotting. (This functionality is currently broken unless running a stop-and-go style scan)

The scripts of import are

1. moller_scan_continuous.sh (This scans the area of the detector with the motor never stopping)
2. mollerScan_alpha.sh (This scans the area of the detector with the motor stopping at each location and moving again)
3. gainScan.sh (This scans 20 select points (one per sector) of our detector at a given voltage)

There is python code to plot output from each script, generate_plot.py and generate_plot_continuous.py, which plot the output of 2. and 1. respectively.

Note there is example script stored in "./scan_control/scanscripts/example_script.sh", with lots of comments that could be modified for an arbitrary detector. 

### How it works

There is an image_frame.py and scan_frame.py. The scan frame controls running scans. Inside of here one can change the scripts that the buttons run if they want to run a differnt type of scan.

The image frame takes whatever plot that is stored in ./scan_control/.tmp/test.gif, and displays it. It also trys running the "generate_plot.py", which attempts to take the current filename and plot it. Only works for position_long currently.

### Issues

1. Note that if one runs the continuous scan, the pa sometimes still writes data. One needs to run "ps -ef | grep paLoop" and kill whatever paLoop process that is running.

## Picoammeter frame

This communicates with the picoammeter via USB using code that's in ~/Products/picologic_libusb/

Whenever the computer is restarted one needs to run 

1. cd ~/Products/picologic_libusb
2. ./start_pa_server.sh

This starts a local server which communicates with the picoammeter.

It works by executing the following command in the command line:

        echo currents | netcat -w 1 -t localhost 50001

Every refresh_rate, it reads in new values using the above command, and does some work to plot them.

### How it works

It runs the above command and plots them. The pa_frame is just the wrapper for both the plot and the table. Inside plot, it runs an animation which every refresh_rate, gets new values, calls the table_frame to set them to the table, and then plot them. It stores the most recent buffer_size values in an array appending new values and deleting the oldest. This handles nothing related to writing the values to file.