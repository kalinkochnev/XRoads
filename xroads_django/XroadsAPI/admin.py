from django.contrib import admin

from XroadsAPI.models import *

# Register your models here.
admin.site.register(Club)
admin.site.register(School)
admin.site.register(District)
admin.site.register(DistrictDomain)
admin.site.register(Event)