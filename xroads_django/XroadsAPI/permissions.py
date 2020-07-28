from typing import List
from XroadsAPI.models import *
from XroadsAPI import permisson_constants as PermConst
from XroadsAPI.permisson_constants import Hierarchy
from django.contrib.contenttypes.models import ContentType


class Role:
    def __init__(self, model_instances=[], permissions=[], **kwargs):
        self.model_instances = model_instances
        self.permissions = permissions

        role = kwargs.get('role', self._match_role(model_instances))
        self.role_hierarchy = self.get_role(role)

    @classmethod
    def create(cls, *model_instances, **kwargs: dict):
        return Role(model_instances=model_instances, **kwargs)

    @property
    def str(self):
        model_ids = [m.id for m in self.model_instances]
        model_info = dict(zip(self.role_hierarchy.level_names, model_ids))
        return self.role_hierarchy.perm_str(**model_info, include_perms=False)

    @classmethod
    def get_role(cls, name) -> PermConst.Hierarchy:
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
    def from_str(cls, perm_ident: str):
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

    def add_perms(self, *permissions):
        self.permissions.extend(permissions)

    def _match_role(self, model_instances):
        inst_names = [inst.__class__.__name__ for inst in model_instances]
        role_name = Hierarchy.match_hierarchy(inst_names, PermConst.ROLES)
        assert role_name is not None, 'Role matcher could not find role with that hierarchy of models'
        return role_name

    def matches(self, input_str):
        pass

    def has_perms(self, input_str, user=None):
        pass
