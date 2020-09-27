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

    def _invite_user(self, email, role, email_func):
        invited_user = None
        try:
            invited_user = InvitedUser.objects.get(email=email)
            invited_user.roles.add(RoleModel.from_role(role))
            return invited_user
        except InvitedUser.DoesNotExist:
            invited_user = InvitedUser.create(email, [role])
            email_func([email])
            return invited_user

    def _add_profile(self, email, role):
        prof = Profile.objects.get(email=email)
        role.give_role(prof)
        return prof

    def _is_updating(self, role: Role, email):
        admins = role.get_admins(perms=['__any__'])
        if admins is not None:
            return admins.filter(email=email).count() == 1

    def add_admin(self, request, hier_role, email_func=None):
        add_admin_form = AddAdminForm(
            data=request.data, hier_role=hier_role)
        if add_admin_form.is_valid():
            email = add_admin_form.validated_data['email']

            club = self.get_object()
            role = Role.from_start_model(club)
            permissions = add_admin_form.validated_data['permissions']
            role.permissions.add(*permissions)

            if self._is_updating(role, email):
                return Response(status=status.HTTP_403_FORBIDDEN)

            if self._can_add_admin(request.user, permissions, role):
                response_data = {}
                # Try to find a user and apply the role to it
                try:
                    prof = self._add_profile(email, role)
                    response_data = EditorSerializer(
                        prof, context={'role': role}).data
                except Profile.DoesNotExist:
                    # If the profile doesn't exist, invite the user and add the role
                    invited = self._invite_user(email, role, email_func)
                    response_data = InvitedUserSerializer(
                        invited, context={'role': role}).data

                return Response(response_data, status=status.HTTP_202_ACCEPTED)

            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=add_admin_form.errors)


class RemoveAdminMixin(BaseAdminMixin):

    def _can_remove_admin(self, request_role, user_role, role):
        if self.modify_perms is None:
            return True

        assert len(request_role.permissions.permissions) == 1
        editable_perms = self.modify_perms[list(request_role.permissions.permissions)[0]]

        data_perms = user_role.permissions.permissions
        for perm in editable_perms:
            if perm in data_perms:
                return True
        return False

    def _remove_invited_user(self, email, role: Role):
        try:
            invited = InvitedUser.objects.get(email=email)
            invited.roles.remove(
                *list(invited.roles.filter(role_name=role.role_str)))
            return Response(status)
        except InvitedUser.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def remove_admin(self, request, has_access=None):
        email_form = RemoveAdminForm(data=request.data)
        if email_form.is_valid():
            email = email_form.validated_data['email']
            role = Role.from_start_model(self.get_object())

            request_role: Role = RoleModel.objects.get(
                profile=request.user, role_name=role.role_str).role
            data_role = None
            try:
                prof = Profile.objects.get(email=email)
                # This gets the role of the request user and the user in question
                data_role: Role = RoleModel.objects.get(
                    profile=prof, role_name=role.role_str).role

                if self._can_remove_admin(request_role, data_role, role):
                    role.remove_role(prof)
                    return Response(status=status.HTTP_202_ACCEPTED)
                return Response({'error': 'You are not allowed to modify this user\'s permissions'}, status=status.HTTP_403_FORBIDDEN)

            except Profile.DoesNotExist:
                data_role: Role = RoleModel.objects.get(inviteduser__email=email, role_name=role.role_str).role
                if self._can_remove_admin(request_role, data_role, role):
                    self._remove_invited_user(email, role)
                    return Response(status=status.HTTP_202_ACCEPTED)
                return Response({'error': 'You are not allowed to modify this user\'s permissions'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=email_form.errors)


class ListAdminMixin(BaseAdminMixin):
    def list_admins(self, request):
        role = Role.from_start_model(self.get_object())
        prof_admins = role.get_admins(perms=['__any__'])
        inv_user_admins = role.get_admins(perms=['__any__'], invited=True)

        user_editors = ListEditorSerializer(
            list(prof_admins), context={'role': role}).data
        invited_editors = InvitedUserSerializer(list(inv_user_admins), context={
                                                'role': role}, many=True).data

        user_editors['admins'].extend(invited_editors)

        return Response(user_editors, status=status.HTTP_200_OK)


class AdminMixin(AddAdminMixin, RemoveAdminMixin, ListAdminMixin):
    pass
