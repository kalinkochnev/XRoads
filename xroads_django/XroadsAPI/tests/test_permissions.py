import pytest
from XroadsAPI.models import *
from XroadsAPI.permissions import Role, Permissions
from XroadsAPI.permisson_constants import Hierarchy
import XroadsAPI.permisson_constants as PermConst
from XroadsAPI.exceptions import *


@pytest.fixture
def role_model_instances(create_club):
    district1 = District.objects.create(id=1, name="d1")
    school1 = School.objects.create(id=1, name="s1")
    club1 = create_club(id=1)

    district1.add_school(school1)
    school1.add_club(club1)

    return (district1, school1, club1)

@pytest.fixture
def perm_const_override():
    PermConst.DISTRICT_ADMIN = 'District Admin'
    PermConst.SCHOOL_ADMIN = 'School Admin'
    PermConst.CLUB_EDITOR = 'Club Editor'
    PermConst.ROLE_HIERARCHY = Hierarchy(District, School, Club, name=PermConst.CLUB_EDITOR)

    PermConst.ROLES = [
        Hierarchy(District, name=PermConst.DISTRICT_ADMIN, poss_perms=['__all__', 'create-school', 'modify-district']),
        Hierarchy(District, School, name=PermConst.SCHOOL_ADMIN, poss_perms=['__all__', 'create-club', 'modify-school', 'hide-school']),
        Hierarchy(District, School, Club, name=PermConst.CLUB_EDITOR, poss_perms=['__all__', 'modify-club', 'add-editor']),
    ]

@pytest.fixture
def perm_test_class(perm_const_override):
    return Permissions([], hierarchy=PermConst.ROLES[0])

class TestPermissionClass:
    def test_add_perms_possible(self, perm_test_class):
        perm = perm_test_class

        perm.add('create-school', 'modify-district')
        perm.add('modify-district')

        assert perm.permissions == {'create-school', 'modify-district'}

    def test_add_perms_illegal(self, perm_test_class):
        perm = perm_test_class

        with pytest.raises(AssertionError):
            assert perm.add('create-school', 'modify-district', 'perm-not-listed-in-hierarchy')

    def test_has_all_perms(self, perm_test_class):
        perm = perm_test_class
        
        assert perm.has_all_perms is False

        perm.allow_all_perms()
        
        assert perm.has_all_perms is True
        assert perm.permissions == {'__all__'}

        perm.permissions = set()
        assert perm.has_all_perms is False
        perm.add('__all__')
        assert perm.has_all_perms is True


    def test_add_perms_already_all(self, perm_const_override):
        test_hier = Hierarchy(District, School, Club, name="test_hier", poss_perms=['some_str', 'other_str'])
        perm = Permissions([], hierarchy=test_hier)

        perm.allow_all_perms()
        perm.add('some_str')

        assert perm.permissions == {'__all__'}

    def test_to_str(self, perm_const_override):
        test_hier = Hierarchy(District, School, Club, name="test_hier", poss_perms=['some_str', 'other_str'])
        perm = Permissions([], hierarchy=test_hier)

        # Putting in a list instead of a set because this test would always fail otherwise. Sets do not preserve order so the str will constantly change
        perm.permissions = ['other_str', 'some_str']

        assert str(perm) == 'perms=[other_str, some_str]'

    def test_has_perms(self, perm_test_class):
        perm = perm_test_class
        assert perm.has_perms(['create-school']) is False

        perm.add('create-school', 'modify-district')
        assert perm.has_perms(['create-school']) is True
        assert perm.has_perms(['create-school', 'modify-district']) is True

        # If permissions not possible for the given hierarchy
        with pytest.raises(AssertionError):
            assert perm.has_perms(['some-perm'])



@pytest.mark.usefixtures("perm_const_override", "db")
class TestRole:

    def test_role_matcher(self, role_model_instances):
        district1, school1, club1 = role_model_instances
        role = Role.create(district1)
        assert role.hierarchy.name == PermConst.DISTRICT_ADMIN

    def test_str_matches(self, role_model_instances, perm_const_override):
        district1, school1, club1 = role_model_instances

        test_hier = Hierarchy(District, School, Club, name="test_hier", poss_perms=['some_str', 'other_str'])
        role = Role.create(district1, school1, club1)
        role.hierarchy = test_hier
        role.permissions.hierarchy = test_hier

        perms = role.hierarchy.poss_perms
        role.permissions.add('some_str', 'other_str')

        expected = 'District-1/School-1/Club-1/perms=[some_str, other_str]'

    def test_role_from_str(self, role_model_instances):
        district1, school1, club1 = role_model_instances

        # The possible perms for School Admins are 'create-club', 'modify-school', 'hide-school'
        role_expected = Role.create(district1, school1)
        
        role_expected.permissions.add('modify-school', 'hide-school')

        perm_str = 'District-1/School-1/perms=[modify-school, hide-school]'
        role_test = Role.from_str(perm_str)

        assert str(role_expected) == str(role_test)

        perm_str = 'District-1/School-1/perms=[]'
        role_test = Role.from_str(perm_str)
        assert role_test.permissions.permissions == set()

    # TODO make a test that checks that the role is valid
    def test_check_role_valid(self):
        pass

    def test_create_role_1_layer(self, role_model_instances):
        district1, school1, club1 = role_model_instances
        role = Role.create(district1, role=PermConst.DISTRICT_ADMIN)
        assert str(role) == 'District-1/perms=[]'

    def test_create_role_2_layers(self, role_model_instances):
        district1, school1, club1 = role_model_instances

        role = Role.create(district1, school1, role=PermConst.SCHOOL_ADMIN)
        assert str(role) == 'District-1/School-1/perms=[]'

    def test_create_role_3_layers(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances

        role = Role.create(district1, school1, club1,
                           role=PermConst.CLUB_EDITOR)
        assert str(role) == 'District-1/School-1/Club-1/perms=[]'

    def test_match_perms_1_layer_multi_param_str(self, role_model_instances):
        district1, school1, club1 = role_model_instances
        
        role = Role.create(district1)
        role.permissions.add('modify-district', 'create-school')
        
        input_str = 'District-1/perms=[modify-district]'
        assert role.is_allowed(role=Role.from_str(input_str)) is True

        input_str = 'District-1/perms=[create-school, modify-district]'
        assert role.is_allowed(role=Role.from_str(input_str)) is True

        input_str = 'District-1/perms=[]'
        assert role.is_allowed(role=Role.from_str(input_str)) is False

    def test_comparison_method(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances

        role1 = Role.create(district1)
        role1.permissions.add('modify-district', 'create-school')
        role2 = Role.create(district1, school1)
        role2.permissions.add('modify-school', 'create-club')
        role3 = Role.create(district1, school1, club1)
        role3.permissions.add('modify-club')

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
        temp_role.permissions.add('modify-district')

        # Test when same level as other role but more perms
        assert role1._comparison(temp_role) == 0

        # Test when same level as other role but fewer perms
        assert temp_role._comparison(role1) == 0

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
        role1.permissions.add('modify-district', 'create-school')
        role2 = Role.create(district1, school1)
        role2.permissions.add('modify-school', 'create-club')
        role3 = Role.create(district1, school1, club1)
        role3.permissions.add('modify-club')

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

        # Test <= and >=
        assert role1 >= role2
        assert role1 >= role1

        assert role2 <= role1
        assert role2 <= role2

    def test_match_perms_3_layer_str(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances

        role = Role.create(district1)
        role.permissions.add('modify-district', 'create-school')

        # Check that School-2 is a part of District-1, and Club-52 is a part of School-2
        input_str = 'District-1/School-1/Club-1/perms=[modify-club]'
        assert Role.from_str(input_str).is_allowed(role=role) == True

        school5 = School.objects.create(id=5, name="s2")
        club52 = create_club(id=52)

        school5.add_club(club52)

        # Check that School-5 is not a part of District-1 and Club-1 not part of School-5, raises exception
        input_str = 'District-1/School-5/Club-52/perms=[update-club]'
        with pytest.raises(InvalidRoleCreated):
            assert role.is_allowed(role=Role.from_str(input_str))

    def test_match_higher_level(self, role_model_instances):
        district1, school1, club1 = role_model_instances

        role = Role.create(district1)

        input_str = 'District-1/School-1/perms=[create-club, modify-school]'

        assert Role.from_str(input_str).is_allowed(role=role) == True

    def test_not_match(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances

        district2 = District.objects.create(id=2, name='d2')
        school4 = School.objects.create(id=4, name="s1")
        club10 = create_club(10)

        district2.add_school(school4)
        school4.add_club(club10)

        role = Role.create(district1, school1, club1)
        role.permissions.add('modify-club')

        input_str = 'District-2/School-4/Club-10/perms=[add-editor]'
        assert role.is_allowed(role=Role.from_str(input_str)) == False

    def test_give_profile_role(self, create_club, create_test_prof, role_model_instances):
        prof = create_test_prof(1)
        district1, school1, club1 = role_model_instances

        role = Role.create(district1, school1, club1)
        role.permissions.add('modify-club')
        role.give_role(prof)

        assert str(role) in [p.perm_name for p in prof.hierarchy_perms.all()]

        role2 = Role.create(district1, school1, club1)
        assert str(role2) not in [p.perm_name for p in prof.hierarchy_perms.all()]


@pytest.mark.usefixtures("db")
class TestHierarchy:
    def test_create_hierarchy(self):
        heirarchy = Hierarchy(District, School, Club, name="Club Editor")

        assert heirarchy.level_names[0] == 'District'
        assert heirarchy.level_names[1] == 'School'
        assert heirarchy.level_names[2] == 'Club'

    def test_get_hier(self):
        PermConst.ROLES = [
            Hierarchy(District, name=PermConst.DISTRICT_ADMIN)
        ]
        assert Hierarchy.get_hierarchy(
            PermConst.DISTRICT_ADMIN) == PermConst.ROLES[0]
