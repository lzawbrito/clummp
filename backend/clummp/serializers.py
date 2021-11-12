from rest_framework import serializers
from .models import Simulation

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ('id', 'mass_ratio', 'impact_parameter', 'proj_axis', 'centroid_distance')