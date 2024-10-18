#! /bin/bash
# Written 6/5/2023 by James Shirk with lots of help from existing sPHENIX codebase

start=`date +%s.%N`
fout=./textfiles/$1
printf "quickScan ${start}\n" > $fout

# The scan might be trash if the starting point is misaligned.
# To avoid this issue we re-initialize the coordinates for EVERY scan...
bash newmotorinit.sh

# set up the serialline to talk tot he motors
[ -z "$SERIALLINE" ] && export SERIALLINE=/dev/ttyUSB0

MODULE=$2
echo "Module = ${MODULE}"

M=5080      # counts per inch of the stepper motor.
M_CM=2000   # counts per cm of stepper motor. Should be easier

# need to change these to fit our module

# I want X0 to be in the middle of the module
X0=50867    #Middle of motor 1 for now
# I want Y0 to be at the top of the module
Y0=3000    # Near the top of motor 1 for now

TH=13.25

THRAD=`echo "${TH}*3.1415926/180.0" | bc -l`
#YTH=128000 #64*2000
YTH=224000 #64*2000
#YTH=300000 #64*2000
# effective beam diameter
WTH=1600

SUM=0
PAIR=0
# These contain the heights of each sector of the active area of the Gem in cm
for i in 4.43 4.17 4.30 4.46 4.67 4.87 5.15 5.50 5.58 5.60
do
    PAIR=`echo "${PAIR}+1" | bc -l`
    printf "about to do a new sector pair\n" > $fout
    X1=$X0
    Y1=`echo "${Y0}+${SUM}" | bc -l`
    echo $Y1
    echo "C,S1M2000,A1M2,S3M2000,A3M2,(IA3M${X1},IA1M${Y1},),R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

    # J determines if it's going to make a left or a right move
    for j in $(seq 1 -2 -1)
    do  
        LR="NAN"
        if [ $j -eq 1 ]
        then
            LR="RIGHT"
        else
            LR="LEFT"
        fi
        printf "PAIR ${PAIR} on ${LR} side\n" > $fout
        
        Y2=`echo "${Y1}+800" | bc -l`
        echo "C,S1M2000,A1M2,S3M2000,A3M2,(IA3M${X1},IA1M${Y2},),R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
        #Y2=$Y1
        CNT=0

        #  OK...now that we are are at the start position, launch the paLoop.sh
        datestring=`date +"%h_%d_%Y_%H-%M-%S"`
        echo "about to launch the pa loop"
        mkdir -p ${SCANS}/${MODULE}
        {
	        paLoop.sh &
        } > ${SCANS}/${MODULE}/${MODULE}_${i}_${j}_${datestring}.txt


        # depending on DY, scan some number of times in each sector
        
        # While true loop
        # Broken when CNT variable is greater than i (in motor units)

        while :
        do
            # special case for top of gem, would be easier if we had like 5 more cm of movement in the motor

            DY=$WTH #0.8*M_CM

            if (( $(echo "$i == 4.43" | bc -l))); then
                DX=`echo "(50.4/2)*${M_CM}" | bc -l`
                X2=`echo "x = ${X0}+${j}*${DX}; scale = 0; x/1" | bc -l`

                printf `date +%s.%N\n` > $fout
                printf "performing move to ${X2}, ${Y2}\n" > $fout

                echo "C,S3M2000,A3M2,IA3M${X2},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

                Y2=`echo "${Y2}+${DY}" | bc -l`
                CNT=`echo "${CNT} + ${DY}" | bc -l`
    
                if (( $(echo "$CNT >= ${i}*${M_CM} - 800" | bc -l))); then
                    break
                fi

                echo "C,S1M2000,A1M2,IA1M${Y2},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE
                echo "C,S3M2000,A3M2,IA3M${X0},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

                printf `date +%s.%N\n` > $fout
                printf "performing move to ${X0}, ${Y2}\n" > $fout

                Y2=`echo "${Y2}+${DY}" | bc -l`
                CNT=`echo "${CNT} + ${DY}" | bc -l`

                if (( $(echo "$CNT >= ${i}*${M_CM} - 800" | bc -l))); then
                    break
                fi
                
                echo "C,S1M2000,A1M2,IA1M${Y2},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE


            else
                # X2 is the final x position given by Y2*Tan(theta)

                # Effectively, from middle of GEM to edge, make a simple left or rightward scan depending on sign of j
                DX=`echo "${j}*(${YTH}-${Y2})*(s(${THRAD})/c(${THRAD}))" | bc -l`
                TAN=`echo "(${YTH}-${Y2})*s(${THRAD})/c(${THRAD})" | bc -l`
                X2=`echo "x = ${X0}+${DX}; scale = 0; x/1" | bc -l`

                printf `date +%s.%N\n` > $fout
                printf "performing move to ${X2}, ${Y2}\n" > $fout

                echo "C,S3M2000,A3M2,IA3M${X2},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

                


                # make a diagonal move down to set up next scan opposite direction of the first
                Y2=`echo "${Y2}+${DY}" | bc -l`
                CNT=`echo "${CNT} + ${DY}" | bc -l`


                if (( $(echo "$CNT >= ${i}*${M_CM} - 800" | bc -l))); then
                    break
                fi

                DX=`echo "${j}*(${YTH}-${Y2})*(s(${THRAD})/c(${THRAD}))" | bc -l`
                X2=`echo "x = ${X0} + ${DX}; scale = 0; x/1" | bc -l`
                echo "C,S1M2000,A1M2,S3M2000,A3M2,(IA3M${X2},IA1M${Y2},),R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

                # make move back to initial position with y shifted downward by DY

                printf `date +%s.%N\n` > $fout
                printf "performing move to ${X2}, ${Y2}\n" > $fout


                echo "C,S3M2000,A3M2,IA3M${X0},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

                # move y down another DY to set up another move from middle to edge
                Y2=`echo "${Y2}+${DY}" | bc -l`
                CNT=`echo "${CNT} + ${DY}" | bc -l`

                if (( $(echo "$CNT >= ${i}*${M_CM} - 800" | bc -l))); then
                    break
                fi
                echo "C,S1M2000,A1M2,IA1M${Y2},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

            fi
        done
    done

    SUM=`echo "${SUM}+(${M_CM}*${i})" | bc -l`
done