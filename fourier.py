#!/usr/bin/env python3

import numpy as np
from PIL import Image
import sys

image = np.asarray(Image.open(sys.argv[1]).convert("P"))
fft = np.fft.fft2(image)
fshift = np.fft.fftshift(fft)
mag_spectrum = 20*np.log(np.abs(fshift))

rows, cols = image.shape
red_const = 300

crow = rows/2
ccol = cols/2

fshift[:int(crow-rows/red_const), :int(ccol-cols/red_const)] = 0
fshift[:int(crow-rows/red_const), int(ccol+cols/red_const):] = 0
fshift[int(crow+rows/red_const):, int(ccol+cols/red_const):] = 0
fshift[int(crow+rows/red_const):, :int(ccol-cols/red_const)] = 0

f_ishift = np.fft.ifftshift(fshift)
img_back = abs(np.fft.ifft2(f_ishift))

result = Image.fromarray((img_back).astype(np.uint8))

result.save(sys.argv[2], "PNG")
