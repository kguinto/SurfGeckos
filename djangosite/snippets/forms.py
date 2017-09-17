from django.forms import ModelForm
from .models import SiteQuery, SiteContaminant


class SiteQueryForm(ModelForm):
    class Meta:
        model = SiteQuery
        fields = ['site_id',
                  'address',
                  'name',
                  'land_use',
                  'groundwater_use',
                  'sw_distance'
                  ]
