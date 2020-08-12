from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
import XroadsAPI.permisson_constants as PermConst
from XroadsAPI.forms import *
from XroadsAuth.models import Profile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

class ModifyAndReadViewset(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `list()` actions.
    """
    pass


class AddAdminMixin(viewsets.GenericViewSet):
    def add_admins(self, request, hier_role):
        admin_role_serializer = AdminRoleForm(data=request.data, hier_role=hier_role)
        if admin_role_serializer.is_valid():
            for prof in admin_role_serializer.profiles:
                obj = self.get_object()
                obj.add_admin(prof, perms=admin_role_serializer.permissions)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=admin_role_serializer.errors)
            
class RemoveAdminMixin(viewsets.GenericViewSet):
    def remove_admins(self, request):
        email_serializer = UserEmailForm(data=request.data)
        if email_serializer.is_valid():
            for prof in email_serializer.profiles:
                obj = self.get_object()
                obj.remove_admin(prof)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=email_serializer.errors)

class AdminMixin(AddAdminMixin, RemoveAdminMixin):
    pass