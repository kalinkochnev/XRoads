import pytest

class PermString:
    def __init__(self, model_ident, role: Role):
        pass

    def append(self, name, value=''):
        pass

    def _create_key_val(self, name, value):
        pass

    def match(self, other_perm):
        pass

class Role:
    pass


def test_create_role():
    District.objects.create()