#! /bin/bash


SERIALLINE=$2
[ -z "$SERIALLINE" ] && export SERIALLINE=/dev/ttyUSB2

#echo "You selected motor ${MOTOR}"
#echo "You selected port ${SERIALLINE}"

echo X > $SERIALLINE; read POSITION_Y < $SERIALLINE;
echo Z > $SERIALLINE; read POSITION_X < $SERIALLINE;

echo "X ${POSITION_X}, Y ${POSITION_Y}"