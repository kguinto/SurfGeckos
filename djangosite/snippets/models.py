from django.db import models


land_use_types = [
    ('unrestricted', 'Unrestricted'),
    ('commercial', 'Commercial/Industrial'),
]

groundwater_use_types = [
    ('drinking', 'drinking'),
    ('nondrinking', 'nondrinking'),
]

sw_distance_types = [
    ('close', '< 150'),
    ('not_close', '>= 150'),
]

# Create your models here.
class Contaminant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    direct_exposure = models.FloatField()

class SiteQuery(models.Model):
    site_id = models.IntegerField()
    address = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    timestamp = models.DateTimeField(editable=False, auto_now=True)
    land_use = models.CharField(max_length=24, choices=land_use_types)
    groundwater_use = models.CharField(max_length=24, choices=groundwater_use_types)
    sw_distance = models.CharField(max_length=24, choices=sw_distance_types)
