from __future__ import annotations

from typing import List, Set

from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions

from . import permisson_constants as PermConst
from .models import Profile, RoleModel, InvitedUser
from .exceptions import RoleNotComparable, InvalidRoleCreated
from .utils import get_parent_model

import XroadsAPI.models as APIModels


class Permissions:
    def __init__(self, perm_strs: List[str], hierarchy):
        self.permissions: Set[str] = set()
        self.hierarchy: PermConst.Hierarchy = hierarchy

        self.add(*perm_strs)

    @property
    def has_all_perms(self):
        return self.permissions == {'__all__'}

    def allow_all_perms(self):
        self.permissions = set(['__all__'])

    def is_allowed(self, given_perms):
        given_perms = set(given_perms)
        if given_perms == {'__all__'}:
            return True

        assert given_perms.issubset(set(
            self.hierarchy.poss_perms)), f'The {given_perms} not possible for this hierarchy: {self.hierarchy}'

        intersection = given_perms.intersection(self.permissions)
        return self.permissions == intersection

    def add(self, *perms):
        poss_perms = set(self.hierarchy.poss_perms)
        perms = set(perms)

        assert perms.issubset(poss_perms) or perms == {
        }, f'The {perms} not legal for this hierarchy: {self.hierarchy.name}'

        if self.has_all_perms:
            return

        if '__all__' in perms:
            self.allow_all_perms()
            return

        self.permissions.update(set(perms))

    def remove(self, *perms):
        poss_perms = set(self.hierarchy.poss_perms)
        perms = set(perms)

        assert perms.issubset(poss_perms) or perms == {
        }, f'The {perms} not legal for this hierarchy: {self.hierarchy.name}'

        if '__all__' in perms:
            self.permissions.clear()
            return

        if self.has_all_perms:
            new_perms = poss_perms.difference({'__all__', *perms})
            self.permissions = new_perms
            return

        self.permissions.difference_update(perms)

    def __str__(self):
        perm_str = ', '.join(map(str, sorted(self.permissions)))
        return f'perms=[{perm_str}]'

    def __contains__(self, item):
        return item in self.permissions


class Role:
    def __init__(self, model_instances=[], **kwargs):
        self.model_instances = model_instances

        role = kwargs.get('role', self._role_matcher(model_instances))
        self.hierarchy = PermConst.Hierarchy.get_hierarchy(role)

        perms = kwargs.get('permissions', [])
        self.permissions = Permissions(perms, self.hierarchy)

        self.check_role_valid()

    @classmethod
    def create(cls, *model_instances, **kwargs: dict):
        return Role(model_instances=model_instances, **kwargs)

    # IMPORTANT!!! If you are using the from_start_model method, the model needs
    # to have a property that is the same name as the parent class that is all
    # lowercase in order for the relationship to work.
    # Ex: District/School/Club
    #   The school instance has to have a property called: district and the club instance has to have
    #   a property called: school
    @classmethod
    def from_start_model(cls, model_inst):
        """Matches a hierarchy based on the given model and then creates the role based on that hierarchy"""

        # Match hierarchy
        def filter_func(x): return x.highest_level == model_inst.__class__
        hier = list(filter(filter_func, PermConst.ROLES))[0]

        # Get instances based on child. model_instances is backwards
        model_instances = [model_inst]
        for i in range(len(hier.levels)-1, 0, -1):
            parent_model = hier.levels[i-1]
            # It indexes at pos 0 because it inserts the model inst at the start of the inst array once found
            child_inst = model_instances[0]

            # Retrieve the parent model based on parent attribute field name
            parent_inst = getattr(child_inst, parent_model.__name__.lower())

            model_instances.insert(0, parent_inst)

        return Role.create(*model_instances)

    @classmethod
    def from_str(cls, perm_ident: str, perms=[]) -> Role:
        def parse_perms(chunk):
            permissions_str = chunk.split('=')[1]
            removed_brackets = permissions_str.replace(
                '[', '').replace(']', '')
            split_result = removed_brackets.split(', ')
            if split_result == ['']:
                return []
            else:
                return split_result

        def parse_model_inst(chunk):
            # [0] is the model name, [1] is the model id
            model_info = chunk.split('-')
            assert len(
                model_info) == 2, f'The key value pair is incorrect: {model_info}'

            model_type: ContentType = ContentType.objects.get(
                app_label='XroadsAPI', model=model_info[0].lower())
            return model_type.get_object_for_this_type(id=int(model_info[1]))

        split_str = perm_ident.split('/')

        permissions = perms
        model_instances = []
        for chunk in split_str:

            if 'perms=' in chunk and perms == []:
                permissions = parse_perms(chunk)
            else:
                model_instances.append(parse_model_inst(chunk))

        role = cls.create(*model_instances)
        role.permissions.add(*permissions)
        return role

    def go_up_levels(self, times, perms=[]):
        level_index = PermConst.ROLES.index(self.hierarchy)
        assert level_index-times > - \
            1, 'You cannot increase the level by this amount since you will surpass the highest level'

        model_instances = self.model_instances[:len(
            self.model_instances)-times]

        new_role = Role(model_instances=model_instances, permissions=perms)

        return new_role

    def reset_perms(self, perms=[]):
        self.permissions = Permissions(perms, self.hierarchy)

    def _role_matcher(self, model_instances):
        inst_names = [inst.__class__.__name__ for inst in model_instances]
        role_name = PermConst.Hierarchy.match_hierarchy(
            inst_names, PermConst.ROLES)
        assert role_name is not None, 'Role matcher could not find role with that hierarchy of models'
        return role_name

    def is_allowed(self, **kwargs):
        """Returns whether the given user or role instance has permissions for the current role instance"""
        assert len(kwargs) == 1, 'You can only have one key value param'

        keys = kwargs.keys()
        if 'user' in keys:
            return self._is_allowed_user(kwargs['user'])
        elif 'role' in keys:
            return self._is_allowed_role(kwargs['role'])

    def _is_allowed_user(self, user: Profile):
        for role_model in user.roles.all():
            role = role_model.role
            if self._is_allowed_role(role):
                return True
        return False

    def _is_allowed_role(self, role):
        try:
            if role > self:
                return True
            elif role == self:
                return self.permissions.is_allowed(list(role.permissions.permissions))
            else:
                return False
        except RoleNotComparable:
            return False

    def give_role(self, user: Profile):
        role_model = RoleModel.from_role(self)
        self.remove_role(user)
        user.add_roles(role_model)

    def remove_role(self, user: Profile):
        try:
            user.roles.remove(
                *list(user.roles.filter(role_name=self.role_str)))
        except RoleModel.DoesNotExist:
            pass

    def __eq__(self, other_inst: Role):
        return self._comparison(other_inst) == 0

    def __lt__(self, other_inst: Role):
        return self._comparison(other_inst) == -1

    def __le__(self, other_inst: Role):
        comparison = self._comparison(other_inst)
        return comparison == -1 or comparison == 0

    def __gt__(self, other_inst: Role):
        return self._comparison(other_inst) == 1

    def __ge__(self, other_inst: Role):
        comparison = self._comparison(other_inst)
        return comparison == 1 or comparison == 0

    def __str__(self):
        return self.role_str + '/' + str(self.permissions)

    @property
    def role_str(self):
        def key_val_format(key, val):
            return f'{key}-{val}/'

        # * TODO make sure to create regex that tests proper format of string
        model_ids = [m.id for m in self.model_instances]
        model_info = dict(zip(self.hierarchy.level_names, model_ids))

        role_str = ""
        for model_name, model_id in model_info.items():
            role_str += key_val_format(model_name, model_id)

        # Remove the last forward slash
        return role_str[:-1]

    @property
    def highest_level_str(self):
        model_name = self.hierarchy.highest_level.__name__
        model_id = self.model_instances[-1].id
        return f'{model_name}-{model_id}/{self.permissions}'

    def _comparison(self, other_inst):
        # THIS DOES NOT COMPARE PERMISSIONS

        # Raised RoleNotComparable if you try to compare incompatible roles
        self._check_comparable(other_inst)

        # Returns 1 if first is greater, -1 if second is greater, 0 if equal
        if self.model_instances == other_inst.model_instances:
            return 0
        else:
            return self._compare_levels(other_inst)

    def _check_comparable(self, other_inst: Role):
        smaller_len = self if len(self.model_instances) < len(
            other_inst.model_instances) else other_inst
        for i in range(len(smaller_len.model_instances)):
            if other_inst.model_instances[i] != self.model_instances[i]:
                raise RoleNotComparable(
                    'You tried to compare roles with different hierarchys')

    def check_role_valid(self):
        """
        This checks that starting from the top of the model instances, the instances below belong directly to the one above
            Ex: District-1/School-3/Club-5/
            Club-5 must be in School-3 and School-3 must be in District-1
            Distict
        This can query the db quite a few times
        """

        def is_model_contained(child, parent):
            try:
                get_parent_model(child, parent)
                return True
            except inner_m.DoesNotExist:
                return False

        for i in range(len(self.model_instances)-1):
            outer_m = self.model_instances[i]
            inner_m = self.model_instances[i+1]
            if not is_model_contained(inner_m, outer_m):
                raise InvalidRoleCreated(
                    f'Model instance: {inner_m} is not a part of model instance: {outer_m}')

    def _compare_levels(self, other_inst: Role):
        if len(self.model_instances) < len(other_inst.model_instances):
            return 1
        return -1

    def get_admins(self, perms=[], invited=False):
        query_class = Profile if not invited else InvitedUser
        try:
            if '__any__' in perms:
                return query_class.objects.filter(roles__role_name=self.role_str)
            else:
                query_perms = perms if perms != [] else list(
                    self.permissions.permissions)
                role = RoleModel.objects.get(
                    role_name=self.role_str, perms=query_perms)
                return query_class.objects.filter(roles__in=[role])

        except RoleModel.DoesNotExist:
            return []


class BaseMinRole(permissions.BasePermission):

    def get_start_user_attr(self, request, obj):
        return obj

    def has_object_permission(self, request, view, obj):

        # Get the required perms
        permissions = view.hier_perms
        min_admin_role = Role.from_start_model(
            self.get_start_user_attr(request, obj))

        if permissions != '__any__':
            min_admin_role.permissions.add(*permissions)

        user = request.user
        return min_admin_role.is_allowed(user=user) or user.is_superuser


class MinClubEditor(BaseMinRole):
    pass


class MinSchoolRole(BaseMinRole):
    pass


class MinDistrictRole(BaseMinRole):
    pass


class MinSchoolAdminForUser(BaseMinRole):
    def get_start_user_attr(self, request, obj):
        return obj.school
