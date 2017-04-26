#!/usr/bin/env python3

from scipy import absolute, fftpack
from scipy.misc import imsave, imread, imresize
from datetime import datetime as dt
from PIL import Image
import sys

start_time = dt.now()

image = imread(sys.argv[1], mode='RGB')
print("Read: ", dt.now()-start_time)
start_time = dt.now()
image = imresize(image, 0.5, interp='nearest')
print("Rescaled: ", dt.now()-start_time)
start_time = dt.now()
fft = fftpack.fftn(image)
print("Fourier-transformed: ", dt.now()-start_time)
start_time = dt.now()
fshift = fftpack.fftshift(fft)
print("Shifted: ", dt.now()-start_time)
start_time = dt.now()

rows = len(fft)
cols = len(fft[0])
red_const = int(3*cols/4)

crow = rows/2
ccol = cols/2

fshift[:int(crow-rows/red_const), :int(ccol-cols/red_const)] = 0
fshift[:int(crow-rows/red_const), int(ccol+cols/red_const):] = 0
fshift[int(crow+rows/red_const):, int(ccol+cols/red_const):] = 0
fshift[int(crow+rows/red_const):, :int(ccol-cols/red_const)] = 0
print("Reduced information: ", dt.now()-start_time)
start_time = dt.now()

f_ishift = fftpack.ifftshift(fshift)
img_back = fftpack.ifftn(f_ishift)
img_back = absolute(img_back)
print("Retransformed: ", dt.now()-start_time)
start_time = dt.now()

img_back = imresize(img_back, 2.0, interp='nearest')
print("Resized: ", dt.now()-start_time)
start_time = dt.now()

result = imsave(sys.argv[2], img_back)
print("Saved: ", dt.now()-start_time)