#!/bin/sh

[ -z "$SERIALLINE" ] && export SERIALLINE=/dev/serial/by-id/usb-1a86_USB2.0-Ser_-if00-port0

echo "C,I${1}M${2}0,R" > $SERIALLINE; echo "C" > $SERIALLINE

exit