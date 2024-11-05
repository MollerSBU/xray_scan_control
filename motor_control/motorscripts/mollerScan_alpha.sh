#! /bin/bash


start=`date +%y%m%d-%T`
fout=./scans/${start}

# The scan might be trash if the starting point is misaligned.
# To avoid this issue we re-initialize the coordinates for EVERY scan...
bash newmotorinit.sh

touch $fout

#set up the serialline to talk tot he motors
[ -z "$SERIALLINE" ] && export SERIALLINE=/dev/serial/by-id/usb-1a86_USB2.0-Ser_-if00-port0


echo "starting new run"

YTH=224000 #64*2000
XMID=50867
TH=13.25
THRAD=`echo "${TH}*3.1415926/180.0" | bc -l`
STEP_SIZE=2000

#y loop (change to 0)
for i in $( eval echo {78000..100000..$STEP_SIZE} )
do
    echo $i
    sleep 1
    echo "C,IA1M${i},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
    DX=`echo "(${YTH}-${i})*(s(${THRAD})/c(${THRAD}))" | bc -l`
    b=101000
    a=0
    XMAX=`echo "${DX%.*} + ${XMID}" | bc -l`
    XMIN=`echo "${XMID} - ${DX%.*}" | bc -l`
    max=$(( XMAX < b ? XMAX : b ))
    min=$(( XMIN > a ? XMIN : a ))

    if (((i % $((2*$STEP_SIZE))) == 0))
    then
        for j in $( eval echo {$max..$min..$STEP_SIZE} )
        do
            sleep 0.1
            # # move xray to current value of "j" in x direction
            echo "C,IA3M${j},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
            # # print position to output file
            bash readMotor.sh >> ${fout}
            # # take some number of samples at each location
            for k in {0..100..1}
            do
                echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
                sleep 0.01
            done
        done
     else
        for j in $( eval echo {$min..$max..$STEP_SIZE} )
        do
            sleep 0.1
            echo $j
            # # move xray to current value of "j" in x direction
            echo "C,IA3M${j},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
            # # print position to output file
            bash readMotor.sh >> ${fout}
            # # take some number of samples at each location
            for k in {0..100..1}
            do
                echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
                sleep 0.01
            done
        done
    fi
done

bash /home/mollergem/Products/MasterControlMoller/xray/xRayGun_OFF.sh