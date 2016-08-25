#!/bin/bash

FILEPATH="/tmp/screen.png"

import -window root $FILEPATH

#convert -spread 15 -implode 0.4 -negate $FILEPATH $FILEPATH
~/.config/i3/scripts/fourier.py $FILEPATH $FILEPATH

#mute all audio
amixer -q sset Master,0 mute

i3lock --image=$FILEPATH
#rm $FILEPATH
