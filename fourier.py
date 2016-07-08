#!/usr/bin/env python3

import numpy as np
import cv2
import sys

from matplotlib import pyplot as plt

image = cv2.imread(sys.argv[1], 0)
fft = np.fft.fft2(image)
fshift = np.fft.fftshift(fft)
mag_spectrum = 20*np.log(np.abs(fshift))

rows, cols = image.shape
red_const = 350

crow, ccol = rows/2, cols/2
fshift[:int(crow-rows/red_const), :int(ccol-cols/red_const)] = 0
fshift[:int(crow-rows/red_const), int(ccol+cols/red_const):] = 0
fshift[int(crow+rows/red_const):, int(ccol+cols/red_const):] = 0
fshift[int(crow+rows/red_const):, :int(ccol-cols/red_const)] = 0

f_ishift = np.fft.ifftshift(fshift)
img_back = abs(np.fft.ifft2(f_ishift))

color = ('bone', 'prism', 'nipy_spectral', 'terrain', 'gist_stern', 'ocean', 'seismic', 'rainbow')

plt.figure(figsize=(2.16, 1.92), dpi=1000)
cv2.imwrite(sys.argv[2], img_back)
#fig = plt.imshow(img_back, cmap=random.choice(color))

#plt.axis('off')
#fig.axes.get_xaxis().set_visible(False)
#fig.axes.get_yaxis().set_visible(False)
#plt.savefig(sys.argv[2], bbox_inches='tight', pad_inches=0, dpi=1000)
