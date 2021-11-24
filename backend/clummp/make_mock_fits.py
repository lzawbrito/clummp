from astropy.io import fits
import cv2
from random import random 
import matplotlib.pyplot as plt 
from imutils import format_ndarray
from os import path

input = '/home/lzawbrito/PythonProjects/clummp/testdata/fiducial_1to10_b0_hdf5_plt_cnt_0051_proj_z.fits'

input_data = format_ndarray(fits.getdata(input))
input_hdr = fits.getheader(input)

angle = random() * 360
width, height = len(input_data[0]), len(input_data)
center = (random() * width, random() * height)

rot_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=random() + 0.5)
rotated_data = cv2.warpAffine(input_data, rot_matrix, dsize=(width, height))

fig, ax = plt.subplots(1, 2)
ax[0].imshow(input_data)
ax[1].imshow(rotated_data)

hdu = fits.PrimaryHDU(rotated_data)
hdu.writeto(path.join(path.dirname(input), 'modified_' + path.basename(input)))