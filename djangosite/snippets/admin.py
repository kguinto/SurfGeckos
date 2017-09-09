from django.contrib import admin
from .models import Contaminant

# Register your models here.
class ContaminantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'direct_exposure')
    

admin.site.register(Contaminant, ContaminantAdmin)
