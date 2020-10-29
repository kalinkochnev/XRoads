from django.contrib import admin

from XroadsAPI.models import *

# Register your models here.
admin.site.register(Club)
admin.site.register(School)
admin.site.register(District)
admin.site.register(DistrictDomain)

class ClubAdminInline(admin.StackedInline):
    model = Club
    fk_name = "club"
    max_num = 1
    fieldsets = [
        ('Club Data', {'fields': ['next_featured']})
    ]
    readonly_fields = ['next_featured']