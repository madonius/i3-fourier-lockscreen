#!/usr/bin/env python3

#import numpy as np
from scipy import fftpack
from scipy import absolute
from scipy.misc import imsave, imread, imshow
from PIL import Image
import sys

image = imread(sys.argv[1])
fft = fftpack.fftn(image)
fshift = fftpack.fftshift(fft)

rows = len(fft)
cols = len(fft[0])
red_const = int(3*cols/4)

crow, ccol = int(rows/2), int(cols/2)
fshift[:int(crow-rows/red_const), :int(ccol-cols/red_const)] = 0
fshift[:int(crow-rows/red_const), int(ccol+cols/red_const):] = 0
fshift[int(crow+rows/red_const):, int(ccol+cols/red_const):] = 0
fshift[int(crow+rows/red_const):, :int(ccol-cols/red_const)] = 0

f_ishift = fftpack.ifftshift(fshift)
img_back = fftpack.ifftn(f_ishift)
img_back = absolute(img_back)

print(img_back[100])
result = imsave(sys.argv[2], img_back)
#result.save(sys.argv[2], "JPEG", quality=80, optimize=True, progressive=True)
