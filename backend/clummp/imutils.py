import numpy as np 
import cv2

from .exceptions import LevelCurveError
from .mathutils import get_level_curves, get_com, dist, norm 
from scipy import ndimage

LEVEL_CURVES = 10
def format_ndarray(a):
	"""
	Convert an array for usage with cv2. 

	Params
	------
	- `a`: an array-like object
	
	Returns
	------
	The array `a` as a numpy ndarray with type float64.
	"""
	a = np.array(a)
	return a.astype(np.float64)

def rotate(data):
	"""
	Convenience function for formatting image data then applying OpenCV 180 
	degree rotation.

	Params
	------
	- `data`: image data as an array
	
	Returns
	------
	Rotated image data as a numpy ndarray.
	"""
	data = format_ndarray(np.array(data))
	return cv2.rotate(data, cv2.ROTATE_180)

def flip_y(data): 
	"""
	Convenience function for formatting image data then applying OpenCV flip 
	about y axis (i.e., a horizontal flip).

	Params
	------
	- `data`: image data as an array
	
	Returns
	------
	Flipped image data as a numpy ndarray.
	"""
	data = format_ndarray(data)
	return cv2.flip(data, 1)

def flip_x(data): 
	"""
	Convenience function for formatting image data then applying OpenCV flip 
	about x axis (i.e., a vertical flip).

	Params
	------
	- `data`: image data as an array
	
	Returns
	------
	Flipped image data as a numpy ndarray.
	"""
	data = format_ndarray(data)
	return cv2.flip(data, 0)

def simple_transform(data, action):
	"""
	Apply the given transformation to the data. 
	
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
	"""
	Constructs destination triangle for use with affine transformation aligning 
	sources horizontally. Uses level sets to find sources, generates an 
	arbitrary third vertex, then returns a reference triangle such that the 
	sources are horizontally centered in the image, and the midpoint of the 
	segment connecting the two sources is centered vertically. 

	Preserves width, height, and scale of image (i.e., the pixel distance 
	between the two sources).

	Params
	------
	- `im`: Image data as an array
	
	Returns
	------
	A 3-by-2 ndarray containing the three triangle vertices.
	"""
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
	
	if midpoint is None or dcom is None or com1 is None or com2 is None: 
		raise LevelCurveError('No level set with two paths found.')
	# Position reference triangle so that base is horizontal and midpoint 
	# of base is in center. 
	dest_com1 = (- dist(com1, midpoint) + (width / 2), height / 2)
	dest_com2 = (dist(com2, midpoint) + (width / 2), height / 2)
	dest_apex = (width / 2, height / 2 + norm(dcom))

	dest_tri = np.array([dest_com1, dest_apex, dest_com2]).astype(np.float32)
	return dest_tri 


def align_image(im, dest_tri, dsize): 
	"""
	Transform the given image such that the two level-curve-obtained sources 
	lie on the first and third coordinates provided by the given destination 
	triangle. 

	Params
	------
	- `im`: image data as an array
	- `dest_tri`: a 3-by-2 array contaning the vertices of the destination 
				  to be used by the affine transformation.
	- `dsize`: the dimensions of the resulting image in pixels.  
	
	Returns
	------
	An ndarray of the transformed image data. 
	"""
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
	"""
	Crop the given image such that the edges of the image are `scale * dist(com1,
	com2))` away from the center. 

	Params
	------
	- `im`: image data as an array
	- `coms`: `(com1, com2)`, the coordinates of the given two sources
	- `scale`: how many times the pixel distance between the sources we will 
				crop away from the center of the image.
	
	Returns
	------
	An ndarray with cropped image data.
	"""
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