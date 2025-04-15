#! /bin/sh

#  Clear out the previously buffered data...
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null


while true
do
    #echo currents | netcat -w 1 -t localhost 50001
    echo currents | netcat -w 1 -t localhost 50001
    sleep 0.02
done
