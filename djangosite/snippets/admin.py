from django.contrib import admin
from .models import Contaminant, SiteQuery, SiteContaminant, ActionLevel

# Register your models here.
class ContaminantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'direct_exposure')
    
class SiteQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'name', 'site_id', 'land_use', 'groundwater_use', 'sw_distance')

admin.site.register(Contaminant, ContaminantAdmin)
admin.site.register(SiteQuery, SiteQueryAdmin)
admin.site.register(SiteContaminant)
admin.site.register(ActionLevel)
