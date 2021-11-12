from .plots import html_plot
from rest_framework.response import Response 
import os
from django.http import JsonResponse

class SimulationPlotMiddleware: 
    def __init__(self, get_response): 
        self.get_response = get_response
    
    def __call__(self, request): 
        response = self.get_response(request) 
        print(response.data[0]['id'])
        
        return JsonResponse({'plot': html_plot()})