import girder_client 
from os import path

BASE_URL = 'https://girder.hub.yt/api/v1/'
AUTH = 'api-auths/creds'
SIMS_FOLDER = '57c8731b7f2483000181b1b3'
DOWNLOAD_PATH = 'data/gcmc/'
FILE_PREFIX = 'fiducial'
FILE_EXT = '.fits.gz'


class ApiQueryError(Exception):
    pass

def query_n_body_catalog(mass_ratio, 
                         imp_param, 
                         t, 
                         proj_axis, 
                         auth):
    query = {
        'mass_ratio': mass_ratio,
        'imp_param': f'b{imp_param}',
        't': '{:04d}'.format(t),
        'proj_axis': proj_axis
        }

    gc = girder_client.GirderClient(apiUrl=BASE_URL)
    username = auth['username']
    password = auth['password']
    gc.authenticate(username, password)

    print('Searching mass ratio folder: ' + query['mass_ratio'])
    mass_ratio_request = gc.listFolder(SIMS_FOLDER, 
        name=f'{query["mass_ratio"]}_{query["imp_param"]}', limit=10)

    try: 
        mass_ratio_folder_id = next(mass_ratio_request)['_id']
    except StopIteration as e: 
        raise ApiQueryError("No mass ratio " + query['mass_ratio_request'] + ".")


    print('Searching elapsed time folder: ' + query['t'])
    elapsed_time_request = gc.listFolder(mass_ratio_folder_id)

    # Note - converts from generator to list
    elapsed_time_request = sorted(elapsed_time_request, key=lambda x: abs(int(x['name']) - int(query['t'])))

    closest_elapsed_time = elapsed_time_request[0]
    elapsed_time_folder_id = closest_elapsed_time['_id']

    # Alter query to contain proper closest time.
    print('Closest elapsed time found: ' + closest_elapsed_time['name'])
    query['t'] = closest_elapsed_time['name']


    sim_file_name = f'{FILE_PREFIX}_{query["mass_ratio"]}' \
                + f'_{query["imp_param"]}' \
                + f'_hdf5_plt_cnt_{query["t"]}' \
                + f'_proj_{query["proj_axis"]}' \
                + FILE_EXT

    print('Searching file container: ' + sim_file_name)
    sim_container_request = gc.listItem(elapsed_time_folder_id, 
                                        name=sim_file_name, 
                                        limit=1)

    sim_file_id = next(gc.listFile(next(sim_container_request)['_id']))['_id']
    print(f'Found file {sim_file_name} with id {sim_file_id}.')
    return sim_file_id, sim_file_name

def download_file(sim_file_id, download_path, auth):

    username = auth['username']
    password = auth['password']
    gc = girder_client.GirderClient(apiUrl=BASE_URL)
    gc.authenticate(username, password)

    print('Downloading file to ' + download_path)
    try: 
        gc.downloadFile(sim_file_id, download_path)
    except FileExistsError as e: 
        print(f'Warning: {download_path} already exists, skipping download.')
        return 

    





