from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SimulationSerializer
from .models import Simulation
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
from django.http import JsonResponse
from .gcmc_api import query_n_body_catalog, download_file
from os import path 
from .utils import unzip, dump_data
from astropy.io import fits
import numpy as np 

data_dir = '/home/lzawbrito/PythonProjects/clummp-old/backend/data/'

class SimulationView(viewsets.ModelViewSet):
    serializer_class = SimulationSerializer
    queryset = Simulation.objects.all()


@csrf_exempt
def CandidatesView(request): 
    data = json.loads(request.body)
    n = data['n']
    obs_path = data['obsPath']
    auth_path = '/home/lzawbrito/PythonProjects/clummp-old/auths/gcmc'

    # Open credentials from given file 
    cred_file = open(auth_path, 'r')
    username, password = [l.replace('\n', '') for l in cred_file.readlines()]
    auth = {'username': username, 'password': password}

    # Query catalog
    file_id, file_name = query_n_body_catalog('1to1', '0', 10, 'x', auth)

    # Dump data 
    dump_data(data_dir)

    download_path = path.join(data_dir, file_name) 
    download_file(file_id, download_path, auth)
    unzipped_data = unzip(download_path)
    obs_data = fits.getdata(obs_path).tolist()
    sim_data = fits.getdata(unzipped_data).tolist()

    # Open credentials from given file 
    cred_file = open(auth_path, 'r')
    username, password = [l.replace('\n', '') for l in cred_file.readlines()]
    auth = {'username': username, 'password': password}

    # Query catalog
    file_id, file_name = query_n_body_catalog('1to1', '0', 10, 'x', auth)

    # Dump data 
    dump_data(data_dir)

    download_path = path.join(data_dir, file_name) 
    download_file(file_id, download_path, auth)
    unzipped_data = unzip(download_path)
    obs_data = fits.getdata(obs_path).tolist()
    sim_data = fits.getdata(unzipped_data).tolist()

    return JsonResponse({'obs': obs_data, 'sim': [sim_data]})

