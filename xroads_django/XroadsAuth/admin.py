from django.contrib import admin

from XroadsAuth.models import HierarchyPerms, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(HierarchyPerms)