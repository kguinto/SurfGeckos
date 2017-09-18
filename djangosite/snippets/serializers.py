from rest_framework import serializers
from .models import Contaminant, SiteQuery


class ContaminantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contaminant
        fields = [
            'id', 'name', 'direct_exposure',
        ]


class SiteQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteQuery
        fields = [
            'site_id', 'address', 'name', 'timestamp',
            'land_use', 'groundwater_use', 'sw_distance',
        ]
