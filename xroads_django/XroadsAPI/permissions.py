from __future__ import annotations

from typing import List, Set
from XroadsAPI.models import *
from XroadsAPI import permisson_constants as PermConst
from XroadsAPI.permisson_constants import Hierarchy
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions


class Permissions:
    def __init__(self, perm_strs: List[str], hierarchy):
        self.permissions: Set[str] = set(perm_strs)
        self.hierarchy: Hierarchy = hierarchy

    def user_has_perms(self, user):
        pass

    def has_perms(self, perms: List[str]):
        pass

    def add(self, *perms):
        self.hierarchy.
        self.permissions.update(set(perms))

    def __str__(self):
        perm_str = ', '.join(map(str, self.permissions))
        return f'perms=[{permissions_no_quotes}]'


class Role:
    def __init__(self, model_instances=[], **kwargs):
        self.model_instances = model_instances

        role = kwargs.get('role', self._match_role(model_instances))
        self.hierarchy = Hierarchy.get_hierarchy(role)

        perms = kwargs.get('permissions', [])
        self.permissions = Permissions(perms, self.hierarchy.name)

        self.check_role_valid()

    @classmethod
    def create(cls, *model_instances, **kwargs: dict):
        return Role(model_instances=model_instances, **kwargs)

    def __str__(self):
        def key_val_format(key, val):
            return f'{key}-{val}/'

        # * TODO make sure to create regex that tests proper format of string
        model_ids = [m.id for m in self.model_instances]
        model_info = dict(zip(self.hierarchy.level_names, model_ids))

        perm_str = ""
        for model_name, model_id in model_info:
            perm_str += add_key_val(model_name, model_id)

        perm_str += str(self.permissions)

        return perm_str

    @classmethod
    def from_str(cls, perm_ident: str) -> Role:
        def parse_perms(chunk):
            permissions_str = chunk.split('=')[1]
            removed_brackets = permissions_str.replace(
                '[', '').replace(']', '')
            return removed_brackets.split(', ')

        def parse_model_inst(chunk):
            # [0] is the model name, [1] is the model id
            model_info = chunk.split('-')
            assert len(
                model_info) == 2, f'The key value pair is incorrect: {model_info}'

            model_type: ContentType = ContentType.objects.get(
                app_label='XroadsAPI', model=model_info[0].lower())
            return model_type.get_object_for_this_type(id=int(model_info[1]))

        split_str = perm_ident.split('/')

        permissions = []
        model_instances = []
        for chunk in split_str:
            if 'perms=' in chunk:
                permissions = parse_perms(chunk)
            else:
                model_instances.append(parse_model_inst(chunk))

        role = cls.create(*model_instances)
        role.permissions.add(*permissions)
        return role

    def _match_role(self, model_instances):
        inst_names = [inst.__class__.__name__ for inst in model_instances]
        role_name = Hierarchy.match_hierarchy(inst_names, PermConst.ROLES)
        assert role_name is not None, 'Role matcher could not find role with that hierarchy of models'
        return role_name

    def has_perms(self, **kwargs):
        def require_kwargs():
            kwarg_keys = list(kwargs.keys())
            arg_error_msg = 'Proper kwargs not provided. Must either be  user  or  role_str'
            assert len(kwargs) == 1, arg_error_msg
            assert 'user' in kwarg_keys or 'role_str' in kwarg_keys, arg_error_msg
            return kwarg_keys[0]
        kwarg_key = require_kwargs()

        if kwarg_key == 'user':
            return self._has_perms_user(user=kwargs['user'])
        return self._has_perms_str(role_str=kwargs['role_str'])

    def _has_perms_user(self, user: Profile):
        perms = user.hierachy_perms.all()
        for perm in perms:
            # ! TODO make sure to check that you are comparing the permissions!!!
            user_role = Role.from_str(perm)
            if perm.perm_name == self.full_str:
                return True
        return False

    def _has_perms_str(self, role_str):
        new_role = Role.from_str(role_str)

        try:
            return self >= new_role
        except RoleNotComparable:
            return False

    def give_role(self, user: Profile):
        perm, created = HierarchyPerms.objects.get_or_create(
            perm_name=self.full_str)
        user.add_perm(perm)

    def is_allowed(self):
        pass

    @classmethod
    def from_start_model(cls, model):
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

        def is_model_contained(inner_m, outer_m):
            # In District-1/School-3/  School-3 is the inner model, District-1 is the outer model
            m2m_query = f'{outer_m.__class__.__name__.lower()}__in'
            m2m_value = [outer_m]

            args = {
                'id': inner_m.id,
                m2m_query: m2m_value,
            }

            try:
                inner_m.__class__.objects.get(**args)
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
