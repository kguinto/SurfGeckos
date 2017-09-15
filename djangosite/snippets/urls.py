from django.conf.urls import url
from . import views

app_name = 'snippets'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sitequery/(?P<sitequery_id>[0-9]+)/$', views.sitequery, name='sitequery'),
    url(r'^sitequery/create/$', views.create_sitequery, name='create_sitequery'),
    url(r'^sitecontaminant/(?P<sitecontaminant_id>[0-9]+)/$', views.sitecontaminant, name='sitecontaminant'),
    url(r'^sitecontaminant/create/(?P<sitequery_id>[0-9]+)$', views.create_sitecontaminant,
        name='create_sitecontaminant'),
]
