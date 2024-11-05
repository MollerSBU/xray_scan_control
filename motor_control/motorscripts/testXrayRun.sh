start=`date +%y%m%d-%T`
fout=./uRwell_Data/${start}

# The scan might be trash if the starting point is misaligned.
# To avoid this issue we re-initialize the coordinates for EVERY scan...
bash newmotorinit.sh

touch $fout

# set up the serialline to talk tot he motors
[ -z "$SERIALLINE" ] && export SERIALLINE=/dev/serial/by-id/usb-1a86_USB2.0-Ser_-if00-port0

#for i in {0..10000..5000}
echo "starting new run"

# this is the y loop
for i in {79000..101000..1000}
do
    sleep 5
    # move xray to current value of "i" in y direction
    echo "C,IA1M${i},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
    # this is the x loop

    echo "moving to y = ${i}" 

    if ((( (i + 1000) % 2000) == 0))
    then
        for j in {31000..53000..1000}
        do
            sleep 0.5
            # move xray to current value of "j" in x direction
            echo "C,IA3M${j},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
            # print position to output file
            bash readMotor.sh >> ${fout}
            # take some number of samples at each location
            for k in {0..100..1}
            do
                echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
                sleep 0.01
            done
        done
    else
        for j in {53000..31000..1000}
        do
            sleep 0.5
            # move xray to current value of "j" in x direction
            echo "C,IA3M${j},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
            # print position to output file
            bash readMotor.sh >> ${fout}
            # take some number of samples at each location
            for k in {0..100..1}
            do
                echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
                sleep 0.01
            done
        done
    fi


done