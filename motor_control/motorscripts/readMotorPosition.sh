#! /bin/bash

#  You must specify which motor
usage() { echo "Usage: $0 [-x] [-y] [-z]" 1>&2; exit 1; }
[ $# -eq 0 ] && usage

while getopts ":xyzXYZ:" option; do
    case $option in
	x) # display Help
            export MOTOR=X
            ;;
	y) # display Help
            export MOTOR=Y
            ;;
	z) # display Help
            export MOTOR=Z
            ;;
	X) # display Help
            export MOTOR=X
            ;;
	Y) # display Help
            export MOTOR=Y
            ;;
	Z) # display Help
            export MOTOR=Z
            ;;
	\?) # Invalid option
            echo "Error: Invalid option"
	    echo "valid options include xyzXYZ"
            exit;;
    esac
done

SERIALLINE=$2
[ -z "$SERIALLINE" ] && export SERIALLINE=/dev/ttyUSB0

#echo "You selected motor ${MOTOR}"
#echo "You selected port ${SERIALLINE}"

echo $MOTOR > $SERIALLINE; read POSITION < $SERIALLINE; echo $POSITION
