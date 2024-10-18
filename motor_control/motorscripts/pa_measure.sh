#! /bin/bash


start=`date +%y%m%d-%T`

fout=./scans/prototype2/sector_current/Sector15${start}


while true
do
    echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
    sleep 0.5
done