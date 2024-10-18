#! /bin/bash

start=`date +%m-%d-%y-%T`
fout=./scans/${start}

##bash newmotorinit.sh

touch $fout
for k in {0..900..1}
            do
                echo currents | netcat -w 1 -t localhost 50001 >> ${fout}
                sleep 1
            done
