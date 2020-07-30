import pytest
from XroadsAPI.models import *
from XroadsAPI.permissions import Role
from XroadsAPI.permisson_constants import Hierarchy
import XroadsAPI.permisson_constants as PermConst
from XroadsAPI.exceptions import *

@pytest.fixture
def perm_const_roles():
    PermConst.ROLES = [
        Hierarchy(District, name=PermConst.DISTRICT_ADMIN),
        Hierarchy(District, School, name=PermConst.SCHOOL_ADMIN),
        Hierarchy(District, School, Club, name=PermConst.CLUB_EDITOR),
    ]


@pytest.fixture
def role_model_instances(create_club):
    district1 = District.objects.create(id=1, name="d1")
    school1 = School.objects.create(id=1, name="s1")
    club1 = create_club(id=1)

    district1.add_school(school1)
    school1.add_club(club1)

    return (district1, school1, club1)


@pytest.mark.usefixtures("perm_const_roles", "db")
class TestRole:
    def test_get_role(self):
        assert Role.get_hierarchy(
            PermConst.DISTRICT_ADMIN) == PermConst.ROLES[0]

    def test_role_matcher(self, role_model_instances):
        district1, school1, club1 = role_model_instances
        role = Role.create(district1)
        assert role.role_hierarchy.name == PermConst.DISTRICT_ADMIN

    def test_check_role_valid(self):
        pass
    # TODO

    def test_create_role_1_layer(self, role_model_instances):
        district1, school1, club1 = role_model_instances
        role = Role.create(district1, role=PermConst.DISTRICT_ADMIN)
        assert role.str == 'District-1/'

    def test_create_role_2_layers(self, role_model_instances):
        district1, school1, club1 = role_model_instances

        role = Role.create(district1, school1, role=PermConst.SCHOOL_ADMIN)
        assert role.str == 'District-1/School-1/'

    def test_create_role_3_layers(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances

        role = Role.create(district1, school1, club1,
                           role=PermConst.CLUB_EDITOR)
        assert role.str == 'District-1/School-1/Club-1/'

    def test_add_perm(self, role_model_instances):
        district1, school1, club1 = role_model_instances

        role = Role.create(district1, role=PermConst.DISTRICT_ADMIN)
        role.add_perms('update-district', 'create-school')

        assert 'update-district' in role.permissions
        assert 'create-school' in role.permissions

    def test_match_perms_1_layer_multi_param_str(self, role_model_instances):
        district1, school1, club1 = role_model_instances

        role = Role.create(district1)
        role.add_perms('update-district', 'create-school')

        input_str = 'District-1/perms=[update-district]'
        assert role.has_perms(role_str=input_str) == True

        input_str = 'District-1/perms=[create-school, update-district]'
        assert role.has_perms(role_str=input_str) == True

        input_str = 'District-1/perms=[create-school, update-district, some-other-perm]'
        assert role.has_perms(role_str=input_str) == False

    def test_comparison_method(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances

        role1 = Role.create(district1)
        role1.add_perms('update-district', 'create-school')
        role2 = Role.create(district1, school1)
        role2.add_perms('update-school', 'create-club')
        role3 = Role.create(district1, school1, club1)
        role3.add_perms('edit-club')

        # Test when exactly equal
        assert role1._comparison(role1) == 0

        # Test when role is higher level than other
        assert role1._comparison(role2) == 1
        assert role1._comparison(role3) == 1
        assert role2._comparison(role3) == 1

        # Test when role is less than other
        assert role3._comparison(role2) == -1
        assert role3._comparison(role1) == -1
        assert role2._comparison(role1) == -1

        temp_role = Role.create(district1)
        temp_role.add_perms('only-one-perm')

        # Test when same level as other role but more perms
        assert role1._comparison(temp_role) == 1

        # Test when same level as other role but fewer perms
        assert temp_role._comparison(role1) == -1

    def test_uncomparable_exception(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances


        district2 = District.objects.create(id=10, name="d2")
        school2 = School.objects.create(id=10, name="s2")
        club2 = create_club(id=10)

        district2.add_school(school2)
        school2.add_club(club2)


        role1 = Role.create(district1)
        role2 = Role.create(district1, school1)
        role3 = Role.create(district1, school1, club1)
        role_a = [role1, role2, role3]

        role4 = Role.create(district2)
        role5 = Role.create(district2, school2)
        role6 = Role.create(district2, school2, club2)
        role_b = [role4, role5, role6]

        for r_a in role_a:
            for r_b in role_b:
                with pytest.raises(RoleNotComparable):
                    assert r_a._check_comparable(r_b)

    def test_comparison_operators(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances

        role1 = Role.create(district1)
        role1.add_perms('update-district', 'create-school')
        role2 = Role.create(district1, school1)
        role2.add_perms('update-school', 'create-club')
        role3 = Role.create(district1, school1, club1)
        role3.add_perms('edit-club')

        # Test when exactly equal
        assert role1 == role1

        # Test when role is higher level than other
        assert role1 > role2
        assert role1 > role3
        assert role2 > role3

        # Test when role is less than other
        assert role3 < role2
        assert role3 < role1
        assert role2 < role1

        temp_role = Role.create(district1)
        temp_role.add_perms('only-one-perm')

        # Test when same level as other role but more perms
        assert role1 > temp_role

        # Test when same level as other role but fewer perms
        assert temp_role < role1

        # Test <= and >=
        assert role1 >= role2
        assert role1 >= role1

        assert role2 <= role1
        assert role2 <= role2

    def test_match_perms_3_layer_str(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances

        role = Role.create(district1)
        role.add_perms('update-district', 'create-school')

        # Check that School-2 is a part of District-1, and Club-52 is a part of School-2
        input_str = 'District-1/School-1/Club-1/perms=[update-club]'
        assert role.has_perms(role_str=input_str) == True


        school5 = School.objects.create(id=5, name="s2")
        club52 = create_club(id=52)

        school5.add_club(club52)

        # Check that School-5 is not a part of District-1 and Club-1 not part of School-5, raises exception
        input_str = 'District-1/School-5/Club-52/perms=[update-club]'
        with pytest.raises(InvalidRoleCreated):
            assert role.has_perms(role_str=input_str)

    def test_match_higher_level(self, role_model_instances):
        district1, school1, club1 = role_model_instances

        role = Role.create(district1)

        input_str = 'District-1/School-1/perms=[create-club, update-school]'

        assert role.has_perms(role_str=input_str) == True

    def test_not_match(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances

        district2 = District.objects.create(id=2, name='d2')
        school4 = School.objects.create(id=4, name="s1")
        club10 = create_club(10)

        district2.add_school(school4)
        school4.add_club(club10)
        
        role = Role.create(district1, school1, club1)
        role.add_perms('edit-club')

        input_str = 'District-2/School-4/Club-10/perms=[edit-clubs]'
        assert role.has_perms(role_str=input_str) == False

    def test_give_profile_role(self, create_club, create_test_prof, role_model_instances):
        prof = create_test_prof(1)
        district1, school1, club1 = role_model_instances

        role = Role.create(district1, school1, club1)
        role.add_perms('edit-club')
        role.give_role(prof)

        assert role.has_perms(user=prof) == True

        role2 = Role.create(district1, school1, club1)
        role2.add_perms('testing-123')
        assert role2.has_perms(user=prof) == False


@pytest.mark.usefixtures("db")
class TestHierarchy:
    def test_create_hierarchy(self):
        heirarchy = Hierarchy(District, School, Club, name="Club Editor")

        assert heirarchy.level_names[0] == 'District'
        assert heirarchy.level_names[1] == 'School'
        assert heirarchy.level_names[2] == 'Club'

    def test_create_perm_str(self):
        heirarchy = Hierarchy(District, School, name="School Admin")
        perm_str = heirarchy.perm_str(District=1, School=2, permissions=[
            'create-blah', 'testing123'])
        assert perm_str == 'District-1/School-2/perms=[create-blah, testing123]'

    def test_role_from_str(self, role_model_instances):
        district1, school1, club1 = role_model_instances

        role_expected = Role.create(district1, school1)
        role_expected.add_perms('create-blah', 'testing123')

        perm_str = 'District-1/School-1/perms=[create-blah, testing123]'
        role_test = Role.from_str(perm_str)

        assert role_expected.str == role_test.str
