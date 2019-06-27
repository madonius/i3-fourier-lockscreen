# Low-Pass Lockscreen

This is a two part configuration for locking your screen with i3lock.

## The Image procedure

First, a screenshot of the display(s) is made.
This screenshot is then read and fouriertransformed.
The result is stripped of its higher frequencies and the result then passed through a reverse fourier pipeline.
On the tested Setups (2160x1200, Full-HD and 1600x800) the result was unreadable yet still, somehow, representing the original content.

### The lockscreen script

Captures the image executes the python script on that image and runs i3lock with that.

### The python script
Does the math with the picture

## Usage

Clone the repository
```bash
mkdir -p $XDG_CONFIG_HOME/i3/scripts/
git checkout https://github.com/madonius/i3-fourier-lockscreen.git
cp fourier.py lockscreen.sh $XDG_CONFIG_HOME/i3/scripts/
```

Edit your configuration file and add
```
# lock the screen
bindsym $mod+i exec $XDG_CONFIG_HOME/i3/scripts/lockscreen.sh
```

Now you may lock your screen by pressing the `modifier` key and `i`

## Licence
GPLv3
