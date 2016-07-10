# Low-Pass Lockscreen

This is a two part configuration for locking your screen with i3lock.

## The Image procedure

First, a screenshot of the display(s) is made. 
This screenshot is then read and fouriertransformed. 
The result is stripped of its higher frequencies and the result then passed through a reverse fourier pipeline.
On the tested Setups (2160x1200, Full-HD and 1600x800) the rsult was unreadable yet still, somehow, reprsenting the original content.

### The lockscreen script

Captures the image executes the python script on that image and runs i3lock with that.

### The python script
Does the maths with the picture

## Licence
GPLv3
