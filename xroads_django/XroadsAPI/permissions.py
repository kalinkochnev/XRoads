from __future__ import annotations

from typing import List
from XroadsAPI.models import *
from XroadsAPI import permisson_constants as PermConst
from XroadsAPI.permisson_constants import Hierarchy
from django.contrib.contenttypes.models import ContentType


class Role:
    def __init__(self, model_instances=[], **kwargs):
        self.model_instances = model_instances
        self.permissions = kwargs.get('permissions', [])

        role = kwargs.get('role', self._match_role(model_instances))
        self.role_hierarchy = self.get_hierarchy(role)
        self.check_role_valid()

    @classmethod
    def create(cls, *model_instances, **kwargs: dict):
        return Role(model_instances=model_instances, **kwargs)

    @property
    def str(self):
        # * TODO make sure to create regex that tests proper format of string
        model_ids = [m.id for m in self.model_instances]
        model_info = dict(zip(self.role_hierarchy.level_names, model_ids))
        return self.role_hierarchy.perm_str(**model_info, include_perms=False)

    @classmethod
    def get_hierarchy(cls, name) -> PermConst.Hierarchy:
        results = cls._filter(
            PermConst.ROLES, lambda x: x.name == name, count=1)
        if len(results) == 0:
            return None
        return results[0]

    @classmethod
    def _filter(cls, obj_list, filter, count=-1):
        # If count is -1 filter all, else filter count
        objs = []
        matched = 0
        for item in obj_list:
            if filter(item):
                objs.append(item)
                matched += 1

            if matched == count:
                break
        return objs

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
        role.add_perms(*permissions)
        return role

    def add_perms(self, *permissions):
        self.permissions.extend(permissions)

    def _match_role(self, model_instances):
        inst_names = [inst.__class__.__name__ for inst in model_instances]
        role_name = Hierarchy.match_hierarchy(inst_names, PermConst.ROLES)
        assert role_name is not None, 'Role matcher could not find role with that hierarchy of models'
        return role_name

    def matches(self, input_str):
        pass

    def has_perms(self, role_str):
        new_role = Role.from_str(role_str)

        try:
            return self >= new_role
        except RoleNotComparable:
            return False

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

    @property
    def highest_level(self):
        return self.model_instances[-1]

    def _comparison(self, other_inst):
        # Raised RoleNotComparable if you try to compare incompatible roles
        self._check_comparable(other_inst)

        # Returns 1 if first is greater, -1 if second is greater, 0 if equal
        if self.model_instances == other_inst.model_instances:
            return self._compare_perms(other_inst)
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
                raise InvalidRoleCreated(f'Model instance: {inner_m} is not a part of model instance: {outer_m}')



    def _compare_levels(self, other_inst: Role):
        if len(self.model_instances) < len(other_inst.model_instances):
            return 1
        return -1

    def _compare_perms(self, other_inst: Role):
        if set(self.permissions) == set(other_inst.permissions):
            return 0
        elif len(self.permissions) > len(other_inst.permissions):
            return 1
        return -1
