import numpy as np 
import cv2
from .mathutils import get_level_curves, get_com, dist, norm 
from scipy import ndimage

LEVEL_CURVES = 10
def format_ndarray(a):
	a = np.array(a)
	return a.astype(np.float64)

def rotate(data):
	data = format_ndarray(np.array(data))
	return cv2.rotate(data, cv2.ROTATE_180)

def flip_y(data): 
	data = format_ndarray(data)
	return cv2.flip(data, 1)

def flip_x(data): 
	data = format_ndarray(data)
	return cv2.flip(data, 0)

def simple_transform(data, action):
	"""
	
	Params
	------
	- `data`: 2d array or list containing image data.
	- `action`: a string representing the transformation to be performed on the 
	            image. One of 
		- `'cw'`: 180 clockwise rotation
		- `'flip-x'`: flip about horizontal axis 
		- `'flip-y'`: flip about vertical axis

	Returns
	------
	Transformed data.
	"""
	if action == 'cw':	
		return rotate(data)
	elif action == 'flip-x':	
		return flip_x(data)
	elif action == 'flip-y':		
		return flip_y(data)
	else: 
		raise ValueError('Inappropriate action for `simple_transform`: ' + action)

def construct_dest_triangle(im): 
	# Format image for usage with cv2
	im = format_ndarray(np.array(im))

	# Obtain paths and order in decreasing level to prioritize contours closer 
	# to highest value (and thus obtain center of mass nearest to light source.)
	paths = get_level_curves(im, LEVEL_CURVES)
	paths.reverse()


	width, height = np.shape(im)

	# Obtain centers of mass and apex from first level set which contains 
	# two paths. 
	com1 = None 
	com2 = None 
	midpoint = None 
	apex = None 
	dcom = None 
	for p in paths: 
		if len(p['paths']) == 2:
			com1 = np.array(get_com(np.transpose(p['paths'][0].vertices)))
			com2 = np.array(get_com(np.transpose(p['paths'][1].vertices)))
			midpoint = ((com1[0] + com2[0]) / 2, (com1[1] + com2[1]) / 2)
			dcom = com2 - com1
			apex = np.array([- dcom[1], dcom[0]]) + np.array(midpoint)
			break 
	
	# Position reference triangle so that base is horizontal and midpoint 
	# of base is in center. 
	dest_com1 = (- dist(com1, midpoint) + (width / 2), height / 2)
	dest_com2 = (dist(com2, midpoint) + (width / 2), height / 2)
	dest_apex = (width / 2, height / 2 + norm(dcom))

	dest_tri = np.array([dest_com1, dest_apex, dest_com2]).astype(np.float32)
	return dest_tri 


def align_image(im, dest_tri, dsize): 
	assert len(dsize) == 2
	width, height = dsize

	# Format image for usage with cv2
	im = format_ndarray(np.array(im))

	# Obtain paths and order in decreasing level to prioritize contours closer 
	# to highest value (and thus obtain center of mass nearest to light source.)
	paths = get_level_curves(im, 10)
	paths.reverse()
	for p in paths: 
		# Find first level curve that has two paths 
		if len(p['paths']) == 2: 
			height, width = len(im), len(im[0])

			# Get centers of masses of two paths at this level
			com1 = get_com(np.transpose(p['paths'][0].vertices))
			com2 = get_com(np.transpose(p['paths'][1].vertices))

			# Midpoint of line from com1 to com2
			midpoint = ((com1[0] + com2[0]) / 2, (com1[1] + com2[1]) / 2)
			midpoint = ((com1[0] + com2[0]) / 2, (com1[1] + com2[1]) / 2)
			dcom = np.array(com2) - np.array(com1)
			apex = np.array([- dcom[1], dcom[0]]) + np.array(midpoint)

			# Construct input triangle, perform affine transformation
			src_tri = np.array([com1, apex, com2]).astype(np.float32)
			warp_mat = cv2.getAffineTransform(src_tri, dest_tri)
			trans_image = cv2.warpAffine(im, warp_mat, dsize=(width, height))
			return trans_image	
			
	
def crop(im, coms, scale):
	im = format_ndarray(np.array(im))
	width, height = np.shape(im)
	coms = np.array(coms)
	dcom = np.array(coms[0]) - np.array(coms[1])
	dcom_norm = norm(np.array(dcom))
	try:
		low_height = int(height / 2 - scale * dcom_norm)
		high_height = int(height / 2 + scale * dcom_norm)
		left_width = int(width / 2 - scale * dcom_norm)
		right_width = int(width / 2 + scale * dcom_norm)
		return im[low_height:high_height, left_width:right_width]
	except IndexError:
		return im