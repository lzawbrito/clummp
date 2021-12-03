from django.shortcuts import render
from rest_framework import viewsets

import traceback
from .exceptions import BadFilenameError, LevelCurveError
from .serializers import SimulationSerializer
from .models import Simulation
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
from django.http import JsonResponse
from .backend_pipeline import run_pipeline, transform_file
import numpy as np 
import json 


class SimulationView(viewsets.ModelViewSet):
    serializer_class = SimulationSerializer
    queryset = Simulation.objects.all()

@csrf_exempt 
def TransformView(request, action):
    print(request.GET)
    print(request)
    filename = request.GET.get('filename', default='')
    print(filename)
    trans_data = transform_file(filename, action)
    return JsonResponse(trans_data)


@csrf_exempt
def CandidatesView(request): 
    obs_path = request.GET.get('obsPath', default='')
    n = int(request.GET.get('n', default='1'))
    will_apply_log = request.GET.get('applyLog', default=False)
    print(f'Received request for {n} candidate(s) similar to {obs_path}, with' \
        + f'observation stretching set to {will_apply_log}.')
    try: 
        status = 200
        obs, sims = run_pipeline(obs_path, n, will_apply_log)

        # Convert to list for json serialization
        print('Responding to request.')
        return JsonResponse({'obs': obs.tolist(), 'sims': sims}, status=status)
    except (FileNotFoundError, BadFilenameError): 
        status = 500
        msg = 'Invalid filename.'
        return JsonResponse({'message': msg}, status=status)
    except LevelCurveError:
        status = 500 
        msg = 'Number of sources is not two; check observation file.'
        return JsonResponse({'message': msg}, status=status)
    except Exception as e:
        status = 500
        msg = 'An unexpected error has occurred.'
        traceback.print_exc()
        return JsonResponse({'message': msg}, status=status)



