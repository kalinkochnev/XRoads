import pytest
from XroadsAPI.models import *
from XroadsAPI.tests.test_models import TestClub, TestProfileModel
from django.test import TestCase
from XroadsAPI.permissions import Hierarchy, Role

class TestRole(TestCase):
    def test_get_role(self):
        Role.all_roles = [
            Hierarchy(District, name='District Admin'),
            Hierarchy(District, School, name='School Admin'),
            Hierarchy(District, School, Club, name='School Club'),
        ]

        assert Role().get_role('District Admin') == Role.all_roles[0]

    def test_create_role_1_layer(self):
        level_namesict1 = District.objects.create(name="d1")
        role = Role.create(district1)
        assert role.str == 'District-1/'

    def test_create_role_2_layers(self):
        district1 = District.objects.create(name="d1")
        school1 = School.objects.create(name="s1")

        role = Role.create(district1, school1)
        assert role.str == 'District-1/School-1/'

    def test_create_role_3_layers(self):
        district1 = District.objects.create(name="d1")
        school1 = School.objects.create(name="s1")
        club1 = TestClub.create_test_club()

        role = Role.create(district1, school1, club1)
        assert role.str == 'District-1/School-1/Club-1/'

    def test_add_perm(self):
        district1 = District.objects.create(name="d1")

        role = Role.create(district1, school1)
        role.add_perms('update-district', 'create-school')

        assert 'update-district' in role
        assert 'create-school' in role

    def test_match_perms_1_layer_multi_param_str(self):
        district1 = District.objects.create(name="d1")

        role = Role.create(district1, school1)
        role.add_perms('update-district', 'create-school')

        input_str = 'District-1/perm=[create-district]'
        assert role.has_perms(input_str) == True 

        input_str = 'District-1/perm=[create-district, update-district]'
        assert role.has_perms(input_str) == True

        input_str = 'District-1/perm=[create-district, update-district, some-other-perm]'
        assert role.has_perms(input_str) == False

    def test_match_perms_3_layer_str(self):
        district1 = District.objects.create(id=1, name="d1")
        school2 = School.objects.create(id=2, name='s2')
        club52 = TestClub.create_test_club(id=52)

        role = Role.create(district1)
        role.add_perms('update-district', 'create-school')

        # Check that School-2 is a part of District-1, and Club-52 is a part of School-2
        input_str = 'District-1/School-2/Club-52/perm=[update-club]'
        assert role.has_perms(input_str) == True

        # Check that School-5 is not a part of District-1
        input_str = 'District-1/School-5/Club-52/perm=[update-club]'
        assert role.has_perm(input_str) == False

    def test_match_higher_level(self):
        district1 = District.objects.create(name="d1")

        role = Role.create(district1, school1)
        role.add_perms('create-club', 'update-school')

        input_str = 'District-1/School-1/perm=[create-club, update-school]'

        assert role.has_perms(input_str) == True

    def test_not_match(self):
        district1 = District.objects.create(name="d1")
        school1 = School.objects.create(name="s1")
        club1 = TestClub.create_test_club()

        role = Role.create(district1, school1, club1)
        role.add_perms('edit-club')

        input_str = 'District-2/School-4/Club-1/perms=[edit-clubs]'
        assert role.has_perms(input_str) == False

    def test_give_profile_role(self):
        prof = TestProfileModel.create_test_prof(1)
        district1 = District.objects.create(name="d1")
        school1 = School.objects.create(name="s1")
        club1 = TestClub.create_test_club()

        role = Role.create(district1, school1, club1)
        role.add_perms('edit-club')
        role.give_role(prof)

        assert role.has_perms(user=prof) == True

        role2 = Role.create(district1, school1, club1)
        role2.add_perms('testing-123')
        assert role2.has_perms(user=prof) == False


class TestHierarchy(TestCase):

    def test_create_hierarchy(self):
        heirarchy = Hierarchy(District, School, Club, name="Club Editor")

        assert heirarchy.level_names[0] == 'District'
        assert heirarchy.level_names[1] == 'School'
        assert heirarchy.level_names[2] == 'Club'

    def test_create_perm_str(self):
        heirarchy = Hierarchy(District, School, name="School Admin")
        perm_str = heirarchy.perm_str(District=1, School=2, permissions=['create-blah', 'testing123'])
        assert perm_str == 'District-1/School-2/perms=[create-blah, testing123]'

    @pytest.mark.skip(msg="not done")
    def test_role_from_str(self):
        perm_str = 'District-1/School-2/perms=[create-blah, testing123]'
        role_test = Role.from_str(perm_str)


        district1 = District.objects.create(id=1, name="d1")
        school1 = School.objects.create(id=2, name="s1")
        role_expected = Role.create(district1, school1, club1)
        role.add_perms('create-blah', 'testing123')
        