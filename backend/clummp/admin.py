from django.contrib import admin
from .models import Simulation

# Register your models here.
class SimulationAdmin(admin.ModelAdmin): 
    list_display = ('id', 'mass_ratio', 'impact_parameter', 'proj_axis', 'centroid_distance')


admin.site.register(Simulation, SimulationAdmin)

