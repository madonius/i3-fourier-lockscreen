#!/bin/bash

FILEPATH="/tmp/screenshot.png"

import -window root "$FILEPATH.jpg"
./fourier.py "$FILEPATH.jpg" $FILEPATH

i3lock -f --image=$FILEPATH
rm $FILEPATH*

