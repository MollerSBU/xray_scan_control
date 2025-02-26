#! /bin/bash

VOLTAGE=$1
DIRECTORY=$2
#MODULE=""
#read -p "Enter name of module: " MODULE

echo "$VOLTAGE"
echo "$DIRECTORY"

if [ ! -d "$DIRECTORY" ]; then
  mkdir -p $DIRECTORY
fi

fout=$DIRECTORY/$VOLTAGE

motor_port=$3

# The scan might be trash if the starting point is misaligned.
# To avoid this issue we re-initialize the coordinates for EVERY scan...
bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/newmotorinit.sh $motor_port

touch $fout

#set up the serialline to talk tot he motors
[ -z "$SERIALLINE" ] && export SERIALLINE=$motor_port

echo "init pedestal" >> ${fout}

for k in {0..250..1}
do
    echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
    sleep 0.01
done

echo "starting new run"

#declare -a YARRAY=(9000 18000 23000 33000 42000 51000 61000 72000 83000 94000)

echo "C,IA3M34000,R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

for i in 9000 18000 23000 33000 42000 51000 61000 72000 83000 94000
do
    echo "C,IA1M${i},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
    sleep .1
    bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/readMotor.sh >> ${fout}
    sleep 5
    for k in {0..250..1}
    do
        echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
        sleep 0.01
    done
done

echo "C,IA3M66000,R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

for i in 94000 83000 72000 61000 51000 42000 33000 23000 18000 9000
do
    echo "C,IA1M${i},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
    sleep .1
    bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/readMotor.sh >> ${fout}
    sleep 5
    for k in {0..250..1}
    do
        echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
        sleep 0.01
    done
done

bash /home/mollergem/MOLLER_xray_gui/motor_control/motorscripts/newmotorinit.sh $motor_port
echo "final pedestal" >> ${fout}

for k in {0..250..1}
do
    echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
    sleep 0.01
done

bash /home/mollergem/MOLLER_xray_gui/xray_control/xray/xRayGun_OFF.sh
