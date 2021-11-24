from os import path 
from utils import unzip 
from astropy.io import fits 
import matplotlib.pyplot as plt 
import cv2 
import numpy as np 
from mathutils import get_level_curves
from imutils import align_image, construct_dest_triangle, format_ndarray, crop

auth_path = '/home/lzawbrito/PythonProjects/clummp/auths/gcmc'
obs_data = fits.getdata('/home/lzawbrito/PythonProjects/clummp/testdata/modified_fiducial_1to10_b0_hdf5_plt_cnt_0051_proj_z.fits')

# Open credentials from given file 
cred_file = open(auth_path, 'r')
username, password = [l.replace('\n', '') for l in cred_file.readlines()]
auth = {'username': username, 'password': password}

data_dir = '/home/lzawbrito/PythonProjects/clummp/backend/data/'

id = '57c8cbec7f24830001825b0c'
filename = 'test3.fits.gz'

download_path = path.join(data_dir, filename) 
unzipped_data = unzip(download_path)
sim_data = fits.getdata(unzipped_data)

sims = [sim_data]

print('Converting to float64 arrays...')
# Otherwise incompatible with OpenCV
sims = [s.astype(np.float64) for s in sims]
obs_data = format_ndarray(obs_data)

print('Finding reference image...')
# Find the image with largest area, transform it, and use its transformation as 
# reference for aligned of other images. 
all_ims = sims + [obs_data]
sorted_ims = sorted(all_ims, key=lambda i: len(i[0]) * len(i[1]))
sorted_ims.reverse()
ref = sorted_ims[-1]
ref_paths = get_level_curves(ref, 10)
ref_paths.reverse()

ref_width, ref_height = np.shape(ref)

dest_tri = construct_dest_triangle(ref)

	
print('Aligning data...')
aligned_sims = [align_image(s, dest_tri, dsize=(ref_width, ref_height)) for s in sims]
aligned_obs_data = align_image(obs_data, dest_tri, (ref_width, ref_height))

print('Cropping...')
final_sims = [crop(s, (dest_tri[0], dest_tri[2]), 8) for s in aligned_sims]
final_obs = crop(aligned_obs_data, (dest_tri[0], dest_tri[2]), 8)

fig, ax = plt.subplots(1, len(final_sims) + 2)
ax[0].imshow(obs_data)
ax[1].imshow(final_obs)
k = 2 
for s in final_sims:
	ax[k].imshow(s)
	k += 1

plt.show()