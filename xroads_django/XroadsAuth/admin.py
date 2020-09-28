from django.contrib import admin

from XroadsAuth.models import InvitedUser, Profile, RoleModel

# Register your models here.
admin.site.register(Profile)
admin.site.register(RoleModel)
admin.site.register(InvitedUser)