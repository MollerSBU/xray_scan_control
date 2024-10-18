#! /bin/bash

[ -z "$SERIALLINE" ] && export SERIALLINE=/dev/ttyUSB2

stty -F $SERIALLINE ispeed 9600 ospeed 9600

echo "F" > $SERIALLINE

# Move to limit switch, wait to end, clear the program
echo "C,S1M2000,A1M2,S3M2000,A3M2,(I3M-0,I1M-0,),R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

sleep 1

# Reset origin, wait to end, clear the program 
echo "C,IA1M-0,IA3M-0,R" > $SERIALLINE;  read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

echo "done"
