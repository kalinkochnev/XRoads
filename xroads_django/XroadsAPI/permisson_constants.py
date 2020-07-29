from __future__ import annotations

from XroadsAPI.models import *


class Hierarchy:
    def __init__(self, *models, **kwargs):
        assert 'name' in kwargs, 'Attribute name must be included in keyword args'

        self.name = kwargs['name']
        self.levels: List[models.Model] = models

    @property
    def level_names(self) -> List[models.Model]:
        return [level.__name__ for level in self.levels]

    def perm_str(self, permissions=[], include_perms=True, **kwargs):
        assert self.level_names == list(
            kwargs.keys()), 'Invalid model names were supplied'

        perm_str = ""
        for name in self.level_names:
            model_id = kwargs[name]
            perm_str += self._add_key_val(name, model_id) + '/'

        if include_perms:
            permissions_no_quotes = ', '.join(map(str, permissions))
            return f'{perm_str}perms=[{permissions_no_quotes}]'
        else:
            return perm_str

    def _get_key_val(self, string):
        string.split('-')

    def _add_key_val(self, key, val):
        return f"{key}-{val}"

    @classmethod
    def match_hierarchy(cls, model_names, hier_list):
        for h in hier_list:
            if model_names == h.level_names:
                return h.name
        return None

    def __str__(self):
        return self.name

    @property
    def highest_level(self):
        return self.levels[-1]

DISTRICT_ADMIN = 'District Admin'
SCHOOL_ADMIN = 'School Admin'
CLUB_EDITOR = 'Club Editor'
ROLE_HIERARCHY = Hierarchy(District, School, Club, name=CLUB_EDITOR)


ROLES = [
    Hierarchy(District, name=DISTRICT_ADMIN),
    Hierarchy(District, School, name=SCHOOL_ADMIN),
    Hierarchy(District, School, Club, name=CLUB_EDITOR),
]
