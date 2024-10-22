# MOLLER X-Ray scan control

To run

```
python3 main_control.py
```

## Explanation of control

This section will go over each frame and what every control does

## X-Ray Frame

This section control the x-ray. The x-ray communicates over tcp and will work as long as it's on the same network as the computer.

While ramping up the detector to voltage, HV should be OFF. Prior to turning on the X-Ray for the first time, press "X-Rays: Init".

The default values for the voltage and current should not be deviated from except under special circumstances

After a scan is run, the X-Ray should turn off automatially. In the case of a position dependent gain scan, the motor may stall during the test. In this case, turn the X-ray off as soon as this issue is noticed.

### Some problems and solutions

1. The door/interlock is closed but the frame is still showing interlock as open

        Press the green button on the X-Ray control bin

2. When opening the main control, errors come up about not being able to communicate with the x-ray

        Ensure that the internet cord is plugged in. Try pinging 192.168.1.4. If the computer was restarted the xray server also needs to be restarted. I will add functionality to start this automatically


## Gas Control Frame

This frame allows for control and monitoring of the gas mixing unit. 

The most import thing to watch for are that no errors (bottom left) pop up. The frame will flash red and an error will pop up in the bottom left. This happens if gas flow deviates from what is set by more than 5%.

The control of the flow rate and mixing ratio should mostly remain constnat. Ensure that argon is flowing at ratio \* flow_rate and co2 is flowng at (1-ratio)
\* flow_rate. Mass flow is the important quantity, not volumetric flow.

## Motor Control frame

This frame is rarely used. Sometimes if the motor has not been used in a while or has been unplugged, movement will not work. One can try doing a small movement in x and y to ensure the motor is responsive. The halt button will not work 9 times out of 10. There is no real way to get it to work. You dont have to initialize a new motor before each scan. The scans will do this automatically when run.

### Some problems and solutions

1. The motor is unresponsive and doesnt move when given position and command

        First just make sure that you arent trying to move it to somewhere it already is. If it's not try moving the motor manually using the buttons on the controller. It is also possible for the usb ports of the gas controllers and motor to get mixed up. I plan to fix this.

## Scan Frame

## Picoammeter frame

## Todos (short term) (in relative order of importance)

- Functionality for running scans
-- both position and voltage dependent
- Add more error functionality (all should give pop-ups)
--If gas is off
--count number of sparks?
--motor stopped
- Finish this readme
- Automatically check and assign USB ports

## Todos (long term)

- Dynamic plotting of gain data
- Integrate CAEN HV wrapper into error functionality
