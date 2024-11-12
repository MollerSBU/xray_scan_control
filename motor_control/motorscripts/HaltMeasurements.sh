#! /bin/bash

kill_all_processes () {
    blah=`ps -e | grep $pname`
    length=`echo $blah | wc -c`
    while [ $length -gt 1 ]
    do
	stringarray=(`ps -e | grep $pname`)
	echo "Killing  ${stringarray[0]}"
	kill -9 ${stringarray[0]}
	sleep 0.1
	
	blah=`ps -e | grep $pname`
	length=`echo $blah | wc -c`
	echo $length
    done
}


#  Kill all the paLoops that are writing output files...
pname=paLoop.sh
kill_all_processes

#  Kill all the FastRadialScans...
pname=FastRadialScan
kill_all_processes

#  Kill all the FastRadialScans...
pname=controlledmove
kill_all_processes

pname=mollerScan_alpha.sh
kill_all_processes

#  Stop the motor and return it home.
echo "D" > $1
sleep 2
bash newmotorinit.sh