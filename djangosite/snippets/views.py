from django.shortcuts import render
from django.forms import modelform_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
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

def index(request):
    return render(request, 'snippets/index.html')

def sitequery(request, sitequery_id):
    return HttpResponse("This will show a sitequery for %s" % sitequery_id)

def create_sitequery(request):
    SiteQueryForm = modelform_factory(SiteQuery, exclude=['timestamp'])
    if request.method == 'POST':
        form = SiteQueryForm(request.POST, request.FILES)
        if form.is_valid():
            sitequery = form.save()
            return HttpResponseRedirect(reverse('snippets:sitequery', args=(sitequery.id)))
        else:
            render(request, 'snippets/create_sitequery.html', {'form': form,
            'error_message': 'Something went wrong'})

    else:
        form = SiteQueryForm()
    return render(request, 'snippets/create_sitequery.html', {'form': form})