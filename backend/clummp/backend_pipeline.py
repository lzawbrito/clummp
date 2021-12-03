from os import path, remove 
from astropy.io import fits 
from astropy.visualization import SqrtStretch, simple_norm
from astropy.visualization.stretch import SquaredStretch
import matplotlib.pyplot as plt 
import cv2 
import numpy as np
from .exceptions import BadFilenameError
from .mathutils import get_level_curves
from .imutils import align_image, construct_dest_triangle, crop
from .gcmc_api import download_file
from .utils import unzip, dump_data
from .models import Simulation
from .imutils import simple_transform
import json 

auth_path = '/home/lzawbrito/PythonProjects/clummp/auths/gcmc'
data_dir = '/home/lzawbrito/PythonProjects/clummp/backend/data/'
local_cache = path.join(data_dir, 'cache.json')
CROP_SCALE = 4

def transform_file(filename, action):
    """
    
    Params
    ------
    - `filename`: string, the name of the simulation file we will be 
                transforming
    - `action`: the transformation to perform, one of 
		- `'cw'`: 180 clockwise rotation
		- `'flip-x'`: flip about horizontal axis 
		- `'flip-y'`: flip about vertical axis
    Returns
    ------
    A dict with 
        - `'obs'`: the observation data 
        - `'sims'`: the simulations, with the data corresponding to the given 
            filename transformed as specified by `action`.
    """
    print('Opening file...')
    modified_sims = []
    print('Performing transformation: ' + action)
    sim_data = [] # TODO instead of blank just set to pre-transform
    cache = open(local_cache)
    data = json.load(cache)
    for s in data['sims']:
        if s['name'] == filename: 
            trans_sim_data = simple_transform(s['data'], action)
            modified_sims.append({
                't': s['t'],
                'name': s['name'], 
                'rank': s['rank'], 
                'data': trans_sim_data.tolist(),
                'diff': np.abs(np.array(trans_sim_data) - np.array(data['obs'])).tolist(),
                'id': s['id']
            })
        else: 
            modified_sims.append(s)
    cache.close() 
    remove(local_cache)
    cache_write = open(local_cache, 'w')
    json.dump({'obs': data['obs'], 'sims': modified_sims}, cache_write)

    return {'obs': data['obs'], 'sims': modified_sims}

def	obtain_credentials(path): 
    """
    
    Params
    ------
    - `path`: path to file containing the credentials (username, password 
            separated by newlines)
    
    Returns
    ------
    A dict with: 
        - `'username'`
        - `'password'`
    """
    print('Obtaining credentials...')
    cred_file = open(auth_path, 'r')
    username, password = [l.replace('\n', '') for l in cred_file.readlines()]
    return {'username': username, 'password': password}


def make_query(dist, n):
    """
    Makes a query for `n` simulation rows/tuples ordered by increasing nearness to 
    provided `dist` value. 

    Params
    ------
    - `dist`: number, the dist used to order results 
    - `n`: integer, the number of desired rows
    
    Returns
    ------
    The first `n` entries of the queryset obtained by this query.
    """
    print('Making query to local database...')
    queryset = Simulation.objects.raw("""
        SELECT *
        FROM clummp_simulation 
        ORDER BY abs(centroid_distance - %s) ASC
        """, [dist])
    return queryset[:n]


def download_and_get_data(queryset, auth):
    """
    Download and decode the files in the given queryset. Downloads from GCMC 
    Girder API: https://girder.hub.yt/#collection/57c866a07f2483000181aefa

    Params
    ------
    - `queryset`: a queryset containing the files to download
    - `auth`: a dictionary with `'username'` and `'password'` values to be used 
            for accessing the GCMC API
    
    Returns
    ------
    A list of dicts: 
        - `'name'`: filename 
        - `'t'`: the time field stored in the FITS file in Gyr (billion years)
        - `'id'`: the id of the Girder *container* of the file 
        - `'data'`: an array containing image data of the file
    """
    print('Downloading and unzipping data...')
    sims = []
    for cand in queryset: 
        download_path = path.join(data_dir, cand.filename) 
        download_file(cand.id, download_path, auth)
        unzipped_data = unzip(download_path)
        unzipped_fname = path.basename(unzipped_data)
        sim_data = fits.getdata(unzipped_data)
        sim_hdr = fits.getheader(unzipped_data)
        
        sims.append({
            'name': unzipped_fname, 
            't': sim_hdr['TIME'], 
            'data': sim_data.tolist(),
            'id': cand.container_id
            })
    return sims


def process_ims(sims, obs_data):
    """
    Align image sources, crop images. 

	Find the image with largest area, transform it, and use its transformation as 
	reference for alignment of other images. Pick image with largest area so
	that we do not lose any information from this simulation.

    Params
    ------
    - `sims`: a list of simulation dicts as provided by `download_and_get_data`
    - `obs_data`: the observation data as an array 

    Returns
    ------
    A tuple with 
        - processed observation data
        - a list of dicts: 
            - `'name'`: filename 
            - `'t'`: the time field stored in the FITS file in Gyr (billion years)
            - `'id'`: the id of the Girder *container* of the file 
            - `'data'`: an array containing transformed image data of the file
    """
    print('Processing images...')

	# Find the image with largest area, transform it, and use its transformation as 
	# reference for alignment of other images. Pick image with largest area so
	# that we do not lose any information from this simulation.
    print('---> Finding reference image...')
    all_ims = [s['data'] for s in sims] + [obs_data]

    sorted_ims = sorted(all_ims, key=lambda i: len(i[0]) * len(i[1]))
    # sorted_ims.reverse()
    ref = sorted_ims[-1]

    ref_width, ref_height = np.shape(ref)
    
    dest_tri = construct_dest_triangle(ref)

    print('---> Aligning images...')
	# Align data 
    aligned_sims = []
    for s in sims: 
        aligned = align_image(s['data'], dest_tri, dsize=(ref_width, ref_height)) 
        aligned_sims.append({
            'name': s['name'], 
            't': s['t'], 
            'data': aligned,
            'id': s['id']
        })

    aligned_obs_data = align_image(obs_data, dest_tri, (ref_width, ref_height))
    # Crop 
    print('---> Cropping images...')
    final_sims = []
    for s in aligned_sims:
        cropped = crop(s['data'], (dest_tri[0], dest_tri[2]), CROP_SCALE) 
        final_sims.append({
            'name': s['name'], 
            't': s['t'], 
            'data': cropped,
            'id': s['id']
            })

    final_obs = crop(aligned_obs_data, (dest_tri[0], dest_tri[2]), CROP_SCALE)

    print('---> Done processing images.')
    return final_obs, final_sims


def intensity_scaling(a):
    """
    Apply astropy's normalization and stretching functions to given array. 

    Params
    ------
    - `a`: array to apply scaling
    
    Returns
    ------
    Array with transformation applied. 
    """
    return simple_norm(a, 'log')(a)


def apply_log(sims):
    """
    Convenience function for applying `intensity_scaling` to data fields of 
    simulation dicts.

    Params
    ------
    - `sims`: List of dicts as specified by `download_and_get_data`.
    
    Returns
    ------
    A list of dicts: 
        - `'name'`: filename 
        - `'t'`: the time field stored in the FITS file in Gyr (billion years)
        - `'id'`: the id of the Girder *container* of the file 
        - `'data'`: an array containing image data of the file
    """
    print('Applying logarithmic scale to data...')
    converted_sims = [] 
    for s in sims: 
        converted_sims.append({
            'name': s['name'], 
            't': s['t'], 
            'data': intensity_scaling(s['data']),
            'id': s['id']
        })
    
    return converted_sims


def convert_to_list(sims):
    """
    Convenience function for converting data fields of simulation dicts to 
    Python lists (for JSON serialization). 

    Params
    ------
    - `sims`: List of dicts as specified by `download_and_get_data`.
    
    Returns
    ------
    A list of dicts: 
        - `'name'`: filename 
        - `'t'`: the time field stored in the FITS file in Gyr (billion years)
        - `'id'`: the id of the Girder *container* of the file 
        - `'data'`: an array containing image data of the file
    """
    print('Converting numpy arrays to lists...')
    converted_sims = [] 
    for s in sims: 
        converted_sims.append({
                'name': s['name'], 
                't': s['t'], 
                'data': s['data'].tolist(),
                'diff': s['diff'].tolist(),
                'id': s['id']
            })
    
    return converted_sims

def create_ranks(sims): 
    """
    Adds `'rank'` values to given simulation dicts. Ranked in order of 
    appearance in the list. 

    Params
    ------
    - `sims`: List of dicts as specified by `generate_differences`.
    
    Returns
    ------
    A list of dicts: 
        - `'name'`: filename 
        - `'t'`: the time field stored in the FITS file in Gyr (billion years)
        - `'id'`: the id of the Girder *container* of the file 
        - `'data'`: an array containing image data of the file
    """
    print('Creating ranks...')
    ranked_sims = [] 
    i = 1
    for s in sims: 
        ranked_sims.append({
                'rank': i, 
                'name': s['name'], 
                't': s['t'], 
                'data': s['data'],
                'diff': s['diff'],
                'id': s['id']
            })
        i += 1 
    return ranked_sims

def generate_differences(sims, obs):
    """
    For each simulation dict in `sims` add `'diff'` value computed as 
        abs(sims - obs)

    Params
    ------
    - `sims`: List of dicts as specified by `download_and_get_data`.
    
    Returns
    ------
    A list of dicts: 
        - `'name'`: filename 
        - `'t'`: the time field stored in the FITS file in Gyr (billion years)
        - `'id'`: the id of the Girder *container* of the file 
        - `'data'`: an array containing image data of the file
        - `'diff'`: `abs(sims - obs)`
    """
    print('Computing difference plots...')
    diff_sims = []
    for s in sims: 
            diff_sims.append({
                    'name': s['name'],
                    't': s['t'],
                    'data': s['data'],
                    'diff': np.abs(np.array(s['data']) - np.array(obs)),
                    'id': s['id']
                })
    return diff_sims


def run_pipeline(obs_path, n, will_apply_log):
    """
    Run backend candidate finder pipeline. 

    Params
    ------
    - `obs_path`: path to observation .fits file
    - `n`: number of desired candidate simulations
    - `will_apply_log`: one of `'true'`, `'false'`; whether the pipeline will 
        apply `intensity_scaling` to observation. 

    Returns
    ------
    A tuple with 
        - processed observation data
        - a list of dicts: 
            - `'name'`: filename 
            - `'t'`: the time field stored in the FITS file in Gyr (billion years)
            - `'id'`: the id of the Girder *container* of the file 
            - `'data'`: an array containing transformed image data of the file
            - `'diff'`: `abs(sims - obs)`
    """
    # Obtain credentials 
    auth = obtain_credentials(auth_path)
    
    # Process given observation data
    dist = 1 # TODO dummy value 

	# Query local catalog of simulations 
    candidates = make_query(dist, n)

	# Dump data 
    dump_data(data_dir)

    try: 
        # Download fits files of candidates, unzip them, and store data in array. 
        obs_data = fits.getdata(obs_path)
    except ValueError as e: 
        raise BadFilenameError() from e 

    sims = download_and_get_data(candidates, auth)

    proc_obs, proc_sims = process_ims(sims, obs_data)
    logged_sims = apply_log(proc_sims)
    print('Apply log set to: ' + str(will_apply_log))
    if will_apply_log == 'true':
        proc_obs = intensity_scaling(proc_obs)

    diff_sims = generate_differences(logged_sims, proc_obs)
    ranked_sims = create_ranks(convert_to_list(diff_sims))

    # Save local vertion of this result. 
    print('Saving data locally...')
    f = open(local_cache, 'w') 
    json.dump({'obs': proc_obs.tolist(), 'sims': ranked_sims}, f)
    f.close()
    
    return proc_obs, ranked_sims





