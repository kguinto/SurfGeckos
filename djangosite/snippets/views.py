from django.shortcuts import render
from django.forms import modelform_factory, modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.views.generic import ListView, DetailView
from rest_framework import views, viewsets
from .models import Contaminant, SiteQuery, SiteContaminant
from .serializers import ContaminantSerializer, SiteQuerySerializer

# Create your views here.
class ContaminantList(ListView):
    model = Contaminant

class ContaminantViewSet(viewsets.ModelViewSet):
    model = Contaminant

    queryset = Contaminant.objects.all()
    serializer_class = ContaminantSerializer

class SiteQueryViewSet(viewsets.ModelViewSet):
    model = SiteQuery

    queryset = SiteQuery.objects.all()
    serializer_class = SiteQuerySerializer

class SiteQueryDetail(DetailView):
    model = SiteQuery
    
def index(request):
    return render(request, 'snippets/index.html')

"""def sitequery_pdf(request, pk):
    sitequery = SiteQuery.objects.get(pk=pk)
    context = {'object': sitequery}
    template = 'snippets/sitequery_pdf.html'

    return PDFTemplateResponse(request=request,
                               cmd_options={'disable-javascript':True}, 
                               template=template, 
                               context=context)"""

def sitequery(request, sitequery_id):
    query = SiteQuery()
    return render(request, 'snippets/sitequery_detail.html', {'sitequery': query})

def create_sitequery(request):
    SiteQueryForm = modelform_factory(SiteQuery, exclude=['timestamp'])
    if request.method == 'POST':
        form = SiteQueryForm(request.POST, request.FILES)
        if form.is_valid():
            sitequery = form.save()
            return HttpResponseRedirect(reverse('snippets:create_sitecontaminant', args=(sitequery.id,)))
        else:
            render(request, 'snippets/create_sitequery.html', {'form': form,
            'error_message': 'Something went wrong'})

    else:
        form = SiteQueryForm()
    return render(request, 'snippets/create_sitequery.html', {'form': form})


def sitecontaminant(request, sitecontaminant_id):
    return HttpResponse("This will show a sitecontaminant for %s" % sitecontaminant_id)

def create_sitecontaminant(request, sitequery_id):
    fields = ['contaminant', 'soil', 'gw', 'soil_vapor']
    SiteContaminantFormSet = modelformset_factory(SiteContaminant,
        fields=fields,
        extra=3,
        )
    if request.method == 'POST':
        formset = SiteContaminantFormSet(request.POST, request.FILES)
        if formset.is_valid():
            contaminants = formset.save(commit=False)
            for cont in contaminants:
                cont.sitequery_id = sitequery_id
                cont.save()
            return HttpResponseRedirect(reverse('snippets:sitequery', args=(sitequery_id,)))
        else:
            render(request, 'snippets/create_sitecontaminant.html', {'formset': formset,
            'error_message': 'Something went wrong'})

    else:
        formset = SiteContaminantFormSet(queryset=SiteContaminant.objects.none())
    return render(request, 'snippets/create_sitecontaminant.html', {'formset': formset})
