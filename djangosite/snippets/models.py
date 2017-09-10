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

    __str__ = "Site query for " + str(address)

class ActionLevel(models.Model):
    contaminant = models.ForeignKey(Contaminant, on_delete=models.CASCADE)
    land_use = models.CharField(max_length=24, choices=land_use_types)
    groundwater_use = models.CharField(max_length=24, choices=groundwater_use_types)
    sw_distance = models.CharField(max_length=24, choices=sw_distance_types)
    direct_exposure = models.FloatField()
    soil_vapor_emissions = models.FloatField()
    terrestrial_ecotoxicity = models.FloatField()
    soil_gross_contamination = models.FloatField()
    leaching = models.FloatField()
    dw_toxicity = models.FloatField()
    gw_vapor_emissions = models.FloatField()
    aquatic_ecotoxicity = models.FloatField()
    gw_gross_contamination = models.FloatField()
    shallow_soil_vapor = models.FloatField()
    indoor_air = models.FloatField()

class SiteContaminant(models.Model):
    sitequery = models.ForeignKey(SiteQuery, on_delete=models.CASCADE)
    Contaminant = models.ForeignKey(Contaminant, on_delete=models.CASCADE)
    soil = models.FloatField()
    gw = models.FloatField()
    soil_vapor = models.FloatField()