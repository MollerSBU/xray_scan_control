#! /bin/bash

# gets input from the user to use as the file name and directory where the file will be stored

NAME=$1
DIRECTORY=$2

fout=$DIRECTORY/$NAME

# get the usb port where the motor is connected

motor_port=$3

# The scan might be trash if the starting point is misaligned.
# To avoid this issue we re-initialize the coordinates for EVERY scan...
bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/newmotorinit.sh $motor_port

#initialize output file
touch $fout

#set up the serialline to talk tot he motors
[ -z "$SERIALLINE" ] && export SERIALLINE=$motor_port

# set up the maximum and minimum x values to scan from
xmin=0
xmax=100000

# set the step size of the motor
STEP_SIZE=2000


# This loop below will run over values like so:
# At each position it will record 101 data points to the output file

# (0, 0), (2000, 0), (4000, 0) .... (100000, 0), (100000, 2000), (98000, 2000), .... 


# this will loop over y values like 0, 2000, 4000, 6000, 8000, .... 100000
for i in $( eval echo {0..100000..$STEP_SIZE} )
do
    # move the motor to current value of "i" in y direction
    echo "C,IA1M${i},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

    # We dont want to waste time running from the left to the right every row
    # we make two loops, one L -> R and one R->L depending on where the motor is 
    if (((i % $((2*$STEP_SIZE))) == 0))
    then
        # loop over x positions like xmin, xmin+2000, xmin+4000, ...., xmax
        for j in $( eval echo {$xmin..$xmax..$STEP_SIZE} )
        do
            # sleep just briefly to try to help motor not get stuck
            sleep 0.1
            # # move xray to current value of "j" in x direction
            echo "C,IA3M${j},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
            # # print position to output file
            bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/readMotor.sh >> ${fout}
            # # take some number of samples at each location
            for k in {0..100..1}
            do
                # write current value to output file
                echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
                sleep 0.01
            done
        done
    # same loop just R->L
     else
        for j in $( eval echo {$xmax..$xmin..$STEP_SIZE} )
        do
            sleep 0.1
            echo $j
            # # move xray to current value of "j" in x direction
            echo "C,IA3M${j},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
            # # print position to output file
            bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/readMotor.sh >> ${fout}
            # # take some number of samples at each location
            for k in {0..100..1}
            do
                echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
                sleep 0.01
            done
        done
    fi
done

# turn X-Ray off when we finish
bash /home/mollergem/Products/MasterControlMoller/xray/xRayGun_OFF.sh