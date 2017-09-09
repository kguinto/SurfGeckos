from django.shortcuts import render
from rest_framework import views, viewsets
from .models import Contaminant, SiteQuery
from .serializers import ContaminantSerializer, SiteQuerySerializer

# Create your views here.
class ContaminantViewSet(viewsets.ModelViewSet):
    model = Contaminant

    queryset = Contaminant.objects.all()
    serializer_class = ContaminantSerializer

class SiteQueryViewSet(viewsets.ModelViewSet):
    model = SiteQuery

    queryset = SiteQuery.objects.all()
    serializer_class = SiteQuerySerializer
