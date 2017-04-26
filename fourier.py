#!/usr/bin/env python3

from scipy import absolute, fftpack
from scipy.misc import imsave, imread, imresize
from datetime import datetime as dt
from PIL import Image
import sys

start_time = dt.now()

image = imread(sys.argv[1])
print("Read: ", dt.now()-start_time)
image = imresize(image, 0.5, interp='bilinear')
print("Rescaled: ", dt.now()-start_time)
fft = fftpack.fftn(image)
print("Fourier-transformed: ", dt.now()-start_time)
fshift = fftpack.fftshift(fft)
print("Shifted: ", dt.now()-start_time)

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

f_ishift = fftpack.ifftshift(fshift)
img_back = fftpack.ifftn(f_ishift)
img_back = absolute(img_back)
print("Retransformed: ", dt.now()-start_time)

img_back = imresize(img_back, 2.0, interp='bilinear')
print("Resized: ", dt.now()-start_time)

result = imsave(sys.argv[2], img_back)
print("Saved: ", dt.now()-start_time)