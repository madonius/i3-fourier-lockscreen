#!/bin/bash

FILEPATH="/tmp/screen.png"
FILEPATH_LOCK="/tmp/lockscreen.png"

grim -t png $FILEPATH

#convert -spread 15 -implode 0.4 -negate $FILEPATH $FILEPATH

if [ -z $XDG_CONFIG_HOME ]; then
	XDG_CONFIG_HOME=$HOME/.config
fi

$XDG_CONFIG_HOME/i3/scripts/fourier.py $FILEPATH $FILEPATH_LOCK

#mute all audio
amixer -q sset Master,0 mute

swaylock --tiling --image $FILEPATH_LOCK
rm $FILEPATH
