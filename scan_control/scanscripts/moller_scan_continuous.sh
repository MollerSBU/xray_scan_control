#! /bin/bash

NAME=$1
DIRECTORY=$2

fout=$DIRECTORY/$NAME

motor_port=$3

# The scan might be trash if the starting point is misaligned.
# To avoid this issue we re-initialize the coordinates for EVERY scan...
bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/newmotorinit.sh $motor_port

touch $fout

#set up the serialline to talk tot he motors
[ -z "$SERIALLINE" ] && export SERIALLINE=$motor_port

echo "C,S3M2000, A3M2,R" > $SERIALLINE;


echo "starting new run"

# some calcualtions based on how our detectors taper as a function of y
YTH=224000 #64*2000
XMID=50867
TH=13.25
THRAD=`echo "${TH}*3.1415926/180.0" | bc -l`

STEP_SIZE=2000

{
    bash /home/mollergem/MOLLER_xray_gui/scan_control/scanscripts/paLoop.sh &
} >> $fout

#for i in $( eval echo {0..100000..$STEP_SIZE} )
for i in $( eval echo {60000..100000..$STEP_SIZE} )
do
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
        bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/readMotor.sh >> ${fout}
        #echo $max
        echo "C,IA3M${max},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
        bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/readMotor.sh >> ${fout}
    else
        bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/readMotor.sh >> ${fout}
        #echo $min
        echo "C,IA3M${min},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
        bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/readMotor.sh >> ${fout}
    fi
done

stringarray=(`ps -ef | grep paLoop.sh`)
echo "I will now kill  ${stringarray[1]}"
kill ${stringarray[1]}
echo "completed kill command"
sleep 1
echo "completed sleep"

bash /home/mollergem/Products/MasterControlMoller/xray/xRayGun_OFF.sh