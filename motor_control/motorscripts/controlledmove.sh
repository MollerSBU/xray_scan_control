#!/bin/bash

#
#  Controlled move does the following things:
#        executes a quick move to the specified location
#        waits until the actual location matches the request
#
#

[ -z "$SERIALLINE" ] && export SERIALLINE=/dev/serial/by-id/usb-1a86_USB2.0-Ser_-if00-port0

MOTOR=$2

[ -z "$MOTOR" ] && MOTOR=1

echo "C,IA${MOTOR}M${1},R" > $SERIALLINE; read -n 1 STATUS < $SERIALLINE; echo "C" > $SERIALLINE

exit
