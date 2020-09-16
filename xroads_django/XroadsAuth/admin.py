from django.contrib import admin

from XroadsAuth.models import RoleModel, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(RoleModel)