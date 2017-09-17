from django.db import models

land_use_types = [
    ('unrestricted', 'Unrestricted'),
    ('commercial', 'Commercial/Industrial'),
]

groundwater_use_types = [
    ('drinking', 'Drinking'),
    ('nondrinking', 'Nondrinking'),
]

sw_distance_types = [
    ('close', '< 150m'),
    ('not_close', '>= 150m'),
]


# Create your models here.
class Contaminant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    direct_exposure = models.FloatField()

    def __str__(self):
        return str(self.name)


class SiteQuery(models.Model):
    site_id = models.IntegerField()
    address = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    timestamp = models.DateTimeField(editable=False, auto_now=True)
    land_use = models.CharField(max_length=24, choices=land_use_types)
    groundwater_use = models.CharField(max_length=24, choices=groundwater_use_types)
    sw_distance = models.CharField('Distance from surface water', max_length=24, choices=sw_distance_types)
    
    def __str__(self):
        return "site query for " + str(self.address)


class ActionLevel(models.Model):
    contaminant = models.ForeignKey(Contaminant, on_delete=models.CASCADE)
    land_use = models.CharField(max_length=24, choices=land_use_types)
    groundwater_use = models.CharField(max_length=24, choices=groundwater_use_types)
    sw_distance = models.CharField(max_length=24, choices=sw_distance_types)
    direct_exposure = models.FloatField(blank=True)
    soil_vapor_emissions = models.FloatField(blank=True)
    terrestrial_ecotoxicity = models.FloatField(blank=True)
    soil_gross_contamination = models.FloatField(blank=True)
    leaching = models.FloatField(blank=True)
    dw_toxicity = models.FloatField(blank=True)
    gw_vapor_emissions = models.FloatField(blank=True)
    aquatic_ecotoxicity = models.FloatField(blank=True)
    gw_gross_contamination = models.FloatField(blank=True)
    shallow_soil_vapor = models.FloatField(blank=True)
    indoor_air = models.FloatField(blank=True)

    display_fields = ['direct_exposure', 
                      'soil_vapor_emissions', 
                      'terrestrial_ecotoxicity', 
                      'soil_gross_contamination', 
                      'leaching', 'dw_toxicity', 'gw_vapor_emissions', 
                      'aquatic_ecotoxicity', 'gw_gross_contamination', 
                      'shallow_soil_vapor', 'indoor_air'
                      ]

    def __str__(self):
        s = 'Action levels for '
        s += str(self.contaminant)
        s += ' for ' + str(self.land_use) + ' land use, '
        s += str(self.groundwater_use) + ' groundwater use, and '
        s += str(self.sw_distance) + ' from surface water'

        return s


class SiteContaminant(models.Model):
    sitequery = models.ForeignKey(SiteQuery, on_delete=models.CASCADE)
    contaminant = models.ForeignKey(Contaminant, on_delete=models.CASCADE)
    soil = models.FloatField(verbose_name='Soil (mg/kg)')
    gw = models.FloatField(verbose_name='Groundwater (μg/L)')
    soil_vapor = models.FloatField(verbose_name='Soil Vapor (μg/m³)')

    def action_level(self):
        return ActionLevel.objects.filter(contaminant=self.contaminant,
                                          land_use=self.sitequery.land_use,
                                          groundwater_use=self.sitequery.groundwater_use,
                                          sw_distance=self.sitequery.sw_distance).all()[0]

    def __str__(self):
        return str(self.contaminant.name) + ' at ' + str(self.sitequery)
