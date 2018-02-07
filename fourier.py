#!/usr/bin/env python3

from scipy import absolute, fftpack
from scipy.misc import imsave, imread, imresize
import sys
import time

def fft_row(target, img_row, row_nr):
    """
    :param target:
    :param img_row:
    :param row_nr:
    :return:
    """
    target[row_nr] = fftpack.fft(img_row)

image = imread(sys.argv[1], mode='RGB')
image = imresize(image, 0.5, interp='nearest')

fft_image = [[0] * len(image[0]) for i in range(len(image))]
for line in image:
    linefft = fftpack.fft(line)
    fft_image.append(linefft)

fft = fftpack.fftn(image)
fshift = fftpack.fftshift(fft)

rows = len(fft)
cols = len(fft[0])
red_const = int(3*cols/4)

crow = rows/2
ccol = cols/2

upper_boundary = int(crow - rows / red_const)
lower_boundary = int(crow + rows / red_const)
left_boundary = int(ccol - cols / red_const)
right_boundary = int(ccol + cols / red_const)

fshift[:upper_boundary, :left_boundary] = 0
fshift[:upper_boundary, right_boundary:] = 0
fshift[lower_boundary:, right_boundary:] = 0
fshift[lower_boundary:, :left_boundary] = 0

f_ishift = fftpack.ifftshift(fshift)
img_back = fftpack.ifftn(f_ishift)
img_back = absolute(img_back)

img_back = imresize(img_back, 2.0, interp='nearest')

result = imsave(sys.argv[2], img_back)
