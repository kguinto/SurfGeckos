from django.conf.urls import url
from wkhtmltopdf.views import PDFTemplateView
from . import views

app_name = 'snippets'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sitequery/(?P<pk>[0-9]+)/$', views.SiteQueryDetail.as_view(), name='sitequery_detail'),
    url(r'^sitequery/(?P<sitequery_id>[0-9]+)/$', views.sitequery, name='sitequery'),
    url(r'^sitequery/create/$', views.create_sitequery, name='create_sitequery'),
    url(r'^sitequery/(?P<pk>[0-9]+)/pdf/$', views.sitequery_pdf,
        name='sitequery_pdf'),
    url(r'^sitecontaminant/(?P<sitecontaminant_id>[0-9]+)/$', views.sitecontaminant, name='sitecontaminant'),
    url(r'^sitecontaminant/create/(?P<sitequery_id>[0-9]+)$', views.create_sitecontaminant, name='create_sitecontaminant'),
    url(r'^contaminants/$', views.ContaminantList.as_view(), name='contaminant_list'),
]