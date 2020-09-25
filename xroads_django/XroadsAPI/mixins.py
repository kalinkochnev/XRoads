from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

from XroadsAPI.forms import *
from XroadsAuth.permissions import *
from XroadsAuth.serializers import EditorSerializer, InvitedUserSerializer, ListEditorSerializer
from XroadsAuth.models import InvitedUser
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


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


class AddAdminMixin(BaseAdminMixin):

    def _can_add_admin(self, request_user, user_permissions, role: Role):
        if self.modify_perms is None:
            return True

        request_role: Role = RoleModel.objects.get(
            profile=request_user, role_name=role.role_str).role

        assert len(request_role.permissions.permissions) == 1
        editable_perms = self.modify_perms[list(
            request_role.permissions.permissions)[0]]

        for perm in editable_perms:
            if perm in user_permissions:
                return True
        return False

    def add_admin(self, request, hier_role, email_func=None):
        add_admin_form = AddAdminForm(
            data=request.data, hier_role=hier_role)
        if add_admin_form.is_valid():
            email = add_admin_form.validated_data['email']

            club = self.get_object()
            role = Role.from_start_model(club)
            permissions = add_admin_form.validated_data['permissions']

            if self._can_add_admin(request.user, permissions, role):
                response_data = {}
                try:
                    prof = Profile.objects.get(email=email)
                    role.permissions.add(*permissions)
                    role.give_role(prof)
                    response_data = EditorSerializer(
                        prof, context={'role': role}).data

                except Profile.DoesNotExist:
                    invited_user = None
                    try:
                        invited_user = InvitedUser.objects.get(email=email)
                    except InvitedUser.DoesNotExist:
                        invited_user = InvitedUser.create(email, [role])
                        email_func([email])

                    response_data = InvitedUserSerializer(invited_user, context={'role': role}).data

                return Response(response_data, status=status.HTTP_202_ACCEPTED)

            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=add_admin_form.errors)


class RemoveAdminMixin(BaseAdminMixin):

    def _can_remove_admin(self, request_user, data_user, role: Role):
        if self.modify_perms is None:
            return True

        request_role: Role = RoleModel.objects.get(
            profile=request_user, role_name=role.role_str).role
        data_role: Role = RoleModel.objects.get(
            profile=data_user, role_name=role.role_str).role

        assert len(request_role.permissions.permissions) == 1
        editable_perms = self.modify_perms[list(
            request_role.permissions.permissions)[0]]

        data_perms = data_role.permissions.permissions
        for perm in editable_perms:
            if perm in data_perms:
                return True
        return False

    def remove_admin(self, request, has_access=None):
        email_form = RemoveAdminForm(data=request.data)
        if email_form.is_valid():
            prof = Profile.objects.get(
                email=email_form.validated_data['email'])
            role = Role.from_start_model(self.get_object())

            if self._can_remove_admin(request.user, prof, role):
                role.remove_role(prof)
                return Response(status=status.HTTP_202_ACCEPTED)

            return Response({'error': 'You are not allowed to modify this user\'s permissions'}, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=email_form.errors)


class ListAdminMixin(BaseAdminMixin):
    def list_admins(self, request):
        role = Role.from_start_model(self.get_object())
        prof_admins = role.get_admins(perms=['__any__'])
        inv_user_admins = role.get_admins(perms=['__any__'], invited=True)

        user_editors = ListEditorSerializer(list(prof_admins), context={'role': role}).data
        invited_editors = InvitedUserSerializer(list(inv_user_admins), context={'role': role}, many=True).data

        user_editors['admins'].extend(invited_editors)

        return Response(user_editors, status=status.HTTP_200_OK)


class AdminMixin(AddAdminMixin, RemoveAdminMixin, ListAdminMixin):
    pass
