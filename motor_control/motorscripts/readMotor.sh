#! /bin/bash


SERIALLINE=$2
[ -z "$SERIALLINE" ] && export SERIALLINE=/dev/serial/by-id/usb-1a86_USB2.0-Ser_-if00-port0

#echo "You selected motor ${MOTOR}"
#echo "You selected port ${SERIALLINE}"

echo X > $SERIALLINE; read POSITION_Y < $SERIALLINE;
echo Z > $SERIALLINE; read POSITION_X < $SERIALLINE;

echo "X ${POSITION_X}, Y ${POSITION_Y}"