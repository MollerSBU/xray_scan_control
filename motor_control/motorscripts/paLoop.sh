#! /bin/sh

#  Clear out the previously buffered data...
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null
echo bulk | netcat -w 1 -t localhost 50001 > /dev/null

echo `date +"%h_%d_%Y_%H-%M-%S"`

while true
do
    echo currents | netcat -w 1 -t localhost 50001
    
    sleep 1
done
