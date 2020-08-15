from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
import XroadsAPI.permisson_constants as PermConst
from XroadsAPI.permissions import *
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


class BaseAdminMixin(viewsets.GenericViewSet):
    pass

class AddAdminMixin(BaseAdminMixin):
    # There is no easy way to require to require an add
    def add_admins(self, request, hier_role):
        admin_role_serializer = AdminRoleForm(data=request.data, hier_role=hier_role)
        if admin_role_serializer.is_valid():
            profiles, non_existant_emails = admin_role_serializer.profiles

            for prof in profiles:
                role = Role.from_start_model(self.get_object())
                permissions = admin_role_serializer.validated_data['permissions']
                role.permissions.add(*permissions)

                role.give_role(prof)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=admin_role_serializer.errors)
            
class RemoveAdminMixin(BaseAdminMixin):
    def remove_admins(self, request):
        email_serializer = UserEmailForm(data=request.data)
        if email_serializer.is_valid():
            profiles, non_existant_emails = email_serializer.profiles
            for prof in profiles:
                # TODO make thing that retrieves perm obj for user based on role
                role = Role.from_start_model(self.get_object())
                permissions = admin_role_serializer.validated_data['permissions']
                role.permissions.add(*permissions)
                # FIXME
                role.give_role(prof)
                obj = self.get_object()
                obj.remove_admin(prof)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=email_serializer.errors)

class AdminMixin(AddAdminMixin, RemoveAdminMixin):
    pass