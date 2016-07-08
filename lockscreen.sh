#!/bin/bash

FILEPATH="/etc/i3/pics/screenshot.png"

import -window root $FILEPATH
#ran=$RANDOM
#if [ $ran -lt $(expr 32676 / 2 ) ]
#then
#  convert $FILEPATH -evaluate Multiplicative-noise 6 -evaluate Xor 1337 -implode 0.5 -blur 3 -negate $FILEPATH
#else
#  convert -spread 15 -implode 0.4 -negate $FILEPATH $FILEPATH
#fi
python3 /home/madonius/.config/i3/scripts/fourier.py $FILEPATH $FILEPATH

i3lock -f --image=$FILEPATH
rm $FILEPATH

