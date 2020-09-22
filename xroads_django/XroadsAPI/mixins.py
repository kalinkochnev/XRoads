from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response

from XroadsAPI.forms import *
from XroadsAuth.permissions import *
from XroadsAuth.serializers import EditorSerializer, ListEditorSerializer


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
    modify_perms = None

    def can_modify(self, request_user, data_user, role: Role):
        if self.modify_perms is None:
            return True

        request_role: Role = RoleModel.objects.get(
            profile=request_user, role_name=role.role_str).role
        data_role: Role = RoleModel.objects.get(
            profile=data_user, role_name=role.role_str).role

        assert len(request_role.permissions.permissions) == 1
        editable_perms = self.modify_perms[list(request_role.permissions.permissions)[0]]

        data_perms = data_role.permissions.permissions
        for perm in editable_perms:
            if perm in data_perms:
                return True
        return False


class AddAdminMixin(BaseAdminMixin):
    # There is no easy way to require to require an add
    def update_admin(self, request, hier_role):
        add_admin_form = AddAdminForm(data=request.data, hier_role=hier_role)
        if add_admin_form.is_valid():
            email = add_admin_form.validated_data['email']
            prof = Profile.objects.get(email=email)

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

            data = EditorSerializer(prof, context={'role': role}).data

            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=add_admin_form.errors)


class RemoveAdminMixin(BaseAdminMixin):
    def remove_admin(self, request, has_access=None):
        email_form = RemoveAdminForm(data=request.data)
        if email_form.is_valid():
            prof = Profile.objects.get(
                email=email_form.validated_data['email'])
            role = Role.from_start_model(self.get_object())

            if self.can_modify(request.user, prof, role):
                role.remove_role(prof)
                return Response(status=status.HTTP_202_ACCEPTED)

            return Response({'error': 'You are not allowed to modify this user\'s permissions'}, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=email_form.errors)


class ListAdminMixin(BaseAdminMixin):
    def list_admins(self, request):
        role = Role.from_start_model(self.get_object())
        admins = role.get_admins(perms=['__any__'])

        data = ListEditorSerializer(list(admins), context={'role': role}).data
        return Response(data, status=status.HTTP_200_OK)


class AdminMixin(AddAdminMixin, RemoveAdminMixin, ListAdminMixin):
    pass
