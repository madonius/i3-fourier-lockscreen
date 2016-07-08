#!/bin/bash

FILEPATH="/tmp/screenshot.png"

import -window root $FILEPATH
./fourier.py $FILEPATH $FILEPATH

i3lock -f --image=$FILEPATH
rm $FILEPATH

