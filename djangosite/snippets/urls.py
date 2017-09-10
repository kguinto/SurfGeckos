from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sitequery/(?P<sitequery_id>[0-9]+)/$', views.sitequery, name='sitequery'),
    url(r'^sitequery/create/$', views.create_sitequery, name='create_sitequery'),
]