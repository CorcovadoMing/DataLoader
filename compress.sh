#!/bin/bash

#OPTION=
INPUT=
OUTPUT=

while [ "$#" -gt "0" ]
do

if [ "$1" = "-i" ]; then
    INPUT=$2
    shift 2

elif [ "$1" = "-f" ]; then
    OUTPUT=$2
    shift 2
else
    echo "Usage:"
    echo "compress.sh [-o OUTPUT] [-i INPUT]"
fi

done

# Aggresive compression: XZ_OPT=-9 tar Jcvf $1 $2
# Normal compression: tar czvf $1 $2
tar cvzf $OUTPUT $INPUT 
