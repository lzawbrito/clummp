from django.db import models

# Create your models here.
class Simulation(models.Model): 
    id = models.CharField(max_length=120, primary_key=True)
    filename = models.CharField(max_length=120, default="")
    mass_ratio = models.CharField(max_length=10)
    impact_parameter = models.CharField(max_length=10)
    proj_axis = models.CharField(max_length=1)
    centroid_distance = models.FloatField(default=-1.)
    container_id = models.CharField(max_length=120, default="")

    def _str_(self): 
        return self.id

