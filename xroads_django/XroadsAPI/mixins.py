from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response

from XroadsAPI.forms import *
from XroadsAuth.permissions import *
from XroadsAuth.serializers import EditorSerializer


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
    def add_admin(self, request, hier_role):
        add_admin_form = AddAdminForm(
            data=request.data, hier_role=hier_role)
        if add_admin_form.is_valid():
            email = add_admin_form.validated_data['email']
            
            prof = Profile.objects.get(email=email)
            role = Role.from_start_model(self.get_object())
            permissions = add_admin_form.validated_data['permissions']
            role.permissions.add(*permissions)
            role.give_role(prof)

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=add_admin_form.errors)


class RemoveAdminMixin(BaseAdminMixin):
    def remove_admin(self, request):
        email_form = RemoveAdminForm(data=request.data)
        if email_form.is_valid():
            prof = Profile.objects.get(email=email_form.validated_data['email'])
            role = Role.from_start_model(self.get_object())
            role.remove_role(prof)

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=email_form.errors)

class ListAdminMixin(BaseAdminMixin):
    def list_admins(self, request):
        role = Role.from_start_model(self.get_object())
        admins = role.get_admins(perms=['__any__'])

        data = EditorSerializer(list(admins), context={'role': role}, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class AdminMixin(AddAdminMixin, RemoveAdminMixin, ListAdminMixin):
    pass
