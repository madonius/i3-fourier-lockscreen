#!/usr/bin/env python3

from scipy import absolute, fftpack
from scipy.misc import imsave, imread, imresize
from PIL import Image
import sys

image = imread(sys.argv[1])
image = imresize(image, 0.5, interp='bilinear')
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

img_back = imresize(img_back, 2.0, interp='bilinear')

result = imsave(sys.argv[2], img_back)
#result.save(sys.argv[2], "JPEG", quality=80, optimize=True, progressive=True)
