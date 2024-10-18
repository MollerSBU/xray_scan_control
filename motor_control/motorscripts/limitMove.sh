#!/bin/sh

[ -z "$SERIALLINE" ] && export SERIALLINE=/dev/ttyUSB2

echo "C,I${1}M${2}0,R" > $SERIALLINE; echo "C" > $SERIALLINE

exit