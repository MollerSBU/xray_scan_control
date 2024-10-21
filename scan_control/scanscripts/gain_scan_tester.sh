#! /usr/bin/bash

VOLTAGE=$1
DIRECTORY=$2
#MODULE=""
#read -p "Enter name of module: " MODULE

echo "$VOLTAGE"
echo "$DIRECTORY"

if [ ! -d "$DIRECTORY" ]; then
  mkdir -p $DIRECTORY
fi

fout=$DIRECTORY/$VOLTAGE

touch $fout

echo "hello" >> $fout