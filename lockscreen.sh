#!/bin/bash

FILEPATH="/tmp/screen.png"
FILEPATH_LOCK="/tmp/lockscreen.png"

import -window root $FILEPATH

#convert -spread 15 -implode 0.4 -negate $FILEPATH $FILEPATH
~/.config/i3/scripts/fourier.py $FILEPATH $FILEPATH_LOCK

#mute all audio
amixer -q sset Master,0 mute

i3lock --image=$FILEPATH_LOCK
#rm $FILEPATH
