from __future__ import annotations

import XroadsAPI.models as Models

class Hierarchy:
    def __init__(self, *models, poss_perms=[], **kwargs):
        assert 'name' in kwargs, 'Attribute name must be included in keyword args'

        self.name = kwargs['name']
        self.levels: List[models.Model] = models
        self.poss_perms: List[str] = poss_perms

    @property
    def level_names(self) -> List[models.Model]:
        return [level.__name__ for level in self.levels]

    @classmethod
    def get_hierarchy(cls, name):
        results = list(filter(lambda x: x.name == name, ROLES))
        assert len(results) == 1, 'There are multiple hierarchies with the same name!'

        if len(results) == 0:
            return None
        return results[0]

    @classmethod
    def match_hierarchy(cls, model_names, hier_list):
        """Returns the name of hierarchy object that matches that pattern of models"""
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
ROLE_HIERARCHY = Hierarchy(Models.District, Models.School, Models.Club, name=CLUB_EDITOR)
# TODO create permission constants so then the strings can be changed
# TODO create permission thing that updates the old strings with the renamed strings
# TODO create permission thing that finds permission objects with the same string instead of creating a new permission 
# Roles go from highest level to lowest level in ROLES list 
ROLES = [
    Hierarchy(Models.District, name=DISTRICT_ADMIN, poss_perms=['__all__', 'create-school', 'modify-district', 'add-admin', 'remove-admin']),
    Hierarchy(Models.District, Models.School, name=SCHOOL_ADMIN, poss_perms=['__all__', 'create-club', 'modify-school', 'hide-club', 'view-user-detail', 'hide-school',]),
    Hierarchy(Models.District, Models.School, Models.Club, name=CLUB_EDITOR, poss_perms=['__all__', 'modify-club', 'add-admin']),
]
