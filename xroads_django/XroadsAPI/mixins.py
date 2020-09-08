from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response

from XroadsAPI.forms import *
from XroadsAuth.permissions import *


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
        admin_role_serializer = AdminRoleForm(
            data=request.data, hier_role=hier_role)
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
                role = Role.from_start_model(self.get_object())
                # TODO come up with a better solution using permission model
                for perm in prof.hierarchy_perms.all():
                    if Role.from_str(perm.perm_name) == role:
                        prof.hierarchy_perms.remove(perm)
                        break
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=email_serializer.errors)


class AdminMixin(AddAdminMixin, RemoveAdminMixin):
    pass
