import pytest
from XroadsAPI.models import *
from XroadsAPI.permissions import Role, Permissions
from XroadsAPI.permisson_constants import Hierarchy
import XroadsAPI.permisson_constants as PermConst
from XroadsAPI.exceptions import *


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
            assert perm.add('create-school', 'modify-district',
                            'perm-not-listed-in-hierarchy')

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
        test_hier = Hierarchy(District, School, Club, name="test_hier", poss_perms=[
                              'some_str', 'other_str'])
        perm = Permissions([], hierarchy=test_hier)

        perm.allow_all_perms()
        perm.add('some_str')

        assert perm.permissions == {'__all__'}

    def test_to_str(self, perm_const_override):
        test_hier = Hierarchy(District, School, Club, name="test_hier", poss_perms=[
                              'some_str', 'other_str'])
        perm = Permissions([], hierarchy=test_hier)

        # Putting in a list instead of a set because this test would always fail otherwise. Sets do not preserve order so the str will constantly change
        perm.permissions = ['other_str', 'some_str']

        assert str(perm) == 'perms=[other_str, some_str]'

    def test_has_perms(self, perm_test_class):
        perm = perm_test_class
        assert perm.is_allowed(['create-school']) is True

        perm.add('create-school', 'modify-district')
        assert perm.is_allowed(['create-school']) is False
        assert perm.is_allowed(['create-school', 'modify-district']) is True

        # If permissions not possible for the given hierarchy
        with pytest.raises(AssertionError):
            assert perm.is_allowed(['some-perm'])

    def test_has_perms_more(self, perm_test_class):
        perm = perm_test_class

        # Test list of perms is more than perms of permission class
        perm.add('create-school')
        assert perm.is_allowed(['__all__']) is True
    
    def test_is_allowed_all(self, perm_test_class):
        perm = perm_test_class

        # Test that if given extra perms it is still valid
        perm.add('create-school')
        assert perm.is_allowed(['create-school', 'modify-district']) is True

    def test_remove_all_perms(self, perm_test_class):
        perm = perm_test_class
        perm.add('create-school', 'modify-district')
        assert perm.is_allowed(['create-school', 'modify-district']) is True

        # Test that when all perms are removed there are no permissions left
        perm.remove('__all__')
        assert perm.permissions == set()

    def test_remove_perms_if_all(self, perm_test_class):
        perm: Permissions = perm_test_class
        perm.allow_all_perms()
        assert perm.permissions == {'__all__'}

        # Test that when all perms are removed there are no permissions left
        perm.remove('create-school')
        assert perm.permissions == {'modify-district'}

    def test_normal_remove_perms(self, perm_test_class):
        perm: Permissions = perm_test_class
        perm.add('create-school', 'modify-district')

        perm.remove('create-school')
        assert perm.permissions == {'modify-district'}

@pytest.mark.usefixtures("perm_const_override", "db")
class TestRole:

    def test_role_matcher(self, role_model_instances):
        district1, school1, club1 = role_model_instances()
        role = Role.create(district1)
        assert role.hierarchy.name == PermConst.DISTRICT_ADMIN

    def test_str_matches(self, role_model_instances, perm_const_override):
        district1, school1, club1 = role_model_instances()

        test_hier = Hierarchy(District, School, Club, name="test_hier", poss_perms=[
                              'some_str', 'other_str'])
        role = Role.create(district1, school1, club1)
        role.hierarchy = test_hier
        role.permissions.hierarchy = test_hier

        perms = role.hierarchy.poss_perms
        role.permissions.add('some_str', 'other_str')

        expected = 'District-1/School-1/Club-1/perms=[some_str, other_str]'

    def test_role_from_str(self, role_model_instances):
        d1, s1, c1 = role_model_instances()

        # The possible perms for School Admins are 'create-club', 'modify-school', 'hide-school'
        role_expected = Role.create(d1, s1)

        role_expected.permissions.add('modify-school', 'hide-school')

        perm_str = f'District-{d1.id}/School-{s1.id}/perms=[modify-school, hide-school]'
        role_test = Role.from_str(perm_str)

        assert str(role_expected) == str(role_test)
        perm_str = f'District-{d1.id}/School-{s1.id}/perms=[]'
        role_test = Role.from_str(perm_str)
        assert role_test.permissions.permissions == set()

    # TODO make a test that checks that the role is valid
    def test_check_role_valid(self):
        pass

    def test_create_role_1_layer(self, role_model_instances):
        d1, s1, c1 = role_model_instances()
        role = Role.create(d1, role=PermConst.DISTRICT_ADMIN)
        assert str(role) == f'District-{d1.id}/perms=[]'

    def test_create_role_2_layers(self, role_model_instances):
        d1, s1, c1 = role_model_instances()

        role = Role.create(d1, s1, role=PermConst.SCHOOL_ADMIN)
        assert str(role) == f'District-{d1.id}/School-{s1.id}/perms=[]'

    def test_create_role_3_layers(self, create_club, role_model_instances):
        d1, s1, c1 = role_model_instances()

        role = Role.create(d1, s1, c1, role=PermConst.CLUB_EDITOR)
        assert str(role) == f'District-{d1.id}/School-{s1.id}/Club-{c1.id}/perms=[]'

    def test_is_allowed_perms_1_layer_multi_param_str(self, role_model_instances):
        d1, s1, c1 = role_model_instances()

        role = Role.create(d1)
        role.permissions.add('modify-district', 'create-school')

        input_str = f'District-{d1.id}/perms=[modify-district]'
        assert role.is_allowed(role=Role.from_str(input_str)) is False

        input_str = f'District-{d1.id}/perms=[create-school, modify-district]'
        assert role.is_allowed(role=Role.from_str(input_str)) is True

        input_str = f'District-{d1.id}/perms=[]'
        assert role.is_allowed(role=Role.from_str(input_str)) is False

    def test_comparison_method(self, create_club, role_model_instances):
        district1, school1, club1 = role_model_instances()

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
        district1, school1, club1 = role_model_instances()
        district2, school2, club2 = role_model_instances()

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
        district1, school1, club1 = role_model_instances()

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

    def test_is_allowed_perms_3_layer_str(self, create_club, role_model_instances):
        d1, s1, c1 = role_model_instances()

        role = Role.create(d1)
        role.permissions.add('modify-district', 'create-school')

        # Check that School-2 is a part of District-1, and Club-52 is a part of School-2
        input_str = f'District-{d1.id}/School-{s1.id}/Club-{c1.id}/perms=[modify-club]'
        assert Role.from_str(input_str).is_allowed(role=role) == True

        d2, s2, c2 = role_model_instances()

        # Check that School-5 is not a part of District-1 and Club-1 not part of School-5, raises exception
        input_str = f'District-{d1.id}/School-{s2.id}/Club-{c2.id}/perms=[update-club]'
        with pytest.raises(InvalidRoleCreated):
            assert role.is_allowed(role=Role.from_str(input_str))

    def test_allowed_higher_level(self, role_model_instances):
        d1, s1, c1 = role_model_instances()

        role = Role.create(d1)
        input_str = f'District-{d1.id}/School-{s1.id}/perms=[create-club, modify-school]'

        assert Role.from_str(input_str).is_allowed(role=role) == True

    def test_not_allowed(self, create_club, role_model_instances):
        d1, s1, c1 = role_model_instances()
        d2, s2, c2 = role_model_instances()

        role = Role.create(d1, s1, c1)
        role.permissions.add('modify-club')

        input_str = f'District-{d2.id}/School-{s2.id}/Club-{c2.id}/perms=[add-admin]'
        assert role.is_allowed(role=Role.from_str(input_str)) == False

    def test_give_profile_role(self, create_club, create_test_prof, role_model_instances):
        prof = create_test_prof(1)
        district1, school1, club1 = role_model_instances()

        role = Role.create(district1, school1, club1)
        role.permissions.add('modify-club')
        role.give_role(prof)

        assert str(role) in [p.perm_name for p in prof.hierarchy_perms.all()]

        role2 = Role.create(district1, school1, club1)
        assert str(role2) not in [
            p.perm_name for p in prof.hierarchy_perms.all()]

    def test_from_start_model(self, role_model_instances):
        d1, s1, c1 = role_model_instances()

        district_admin_role = Role.from_start_model(d1)
        assert str(district_admin_role) == f'District-{d1.id}/perms=[]'

        school_admin_role = Role.from_start_model(s1)
        assert str(school_admin_role) == f'District-{d1.id}/School-{s1.id}/perms=[]'

        club_admin_role = Role.from_start_model(c1)
        assert str(club_admin_role) == f'District-{d1.id}/School-{s1.id}/Club-{c1.id}/perms=[]'

    def test_is_allowed_user(self, role_model_instances, create_test_prof):
        prof = create_test_prof(num=1)
        district1, school1, club1 = role_model_instances()

        role = Role.create(district1, school1, club1)
        role.permissions.add('modify-club')

        assert role.is_allowed(user=prof) is False

        role.give_role(prof)
        assert role.is_allowed(user=prof) is True

    def test_reset_perms(self, role_model_instances, create_test_prof):
        district1, school1, club1 = role_model_instances()

        role = Role.create(district1, school1, club1)
        role.permissions.add('modify-club')
        assert role.permissions.permissions == {'modify-club'}

        role.reset_perms()
        assert role.permissions.permissions == set()
        assert role.hierarchy == role.permissions.hierarchy

        role.reset_perms(['modify-club', 'add-admin'])
        assert role.permissions.permissions == {'modify-club', 'add-admin'}

        with pytest.raises(AssertionError):
            assert role.reset_perms(['modify-club', 'blah-blah'])

    def test_move_up_levels(self, role_model_instances, create_test_prof):
        district1, school1, club1 = role_model_instances()

        role = Role.create(district1, school1, club1)
        role.go_up_levels(times=1, perms=['modify-school'])

        assert Role.create(district1, school1) == role
        assert role.permissions.permissions == {'modify-school'}

        role = Role.create(district1, school1, club1)
        role.go_up_levels(times=2, perms=['create-school', 'modify-district'])

        assert Role.create(district1) == role
        assert role.permissions.permissions == {'create-school', 'modify-district'}

        # Goes outside of possible roles
        with pytest.raises(AssertionError):
            role = Role.create(district1, school1, club1)
            assert role.go_up_levels(times=3)
        
        # Permissions not valid for new role
        with pytest.raises(AssertionError):
            role = Role.create(district1, school1, club1)
            assert role.go_up_levels(times=2, perms=['perms not in permissions'])
             
    def test_no_permissions_given(self, role_model_instances, create_test_prof):
        prof = create_test_prof(num=1)
        district1, school1, club1 = role_model_instances()

        role = Role.create(district1, school1, club1)

        assert role.is_allowed(user=prof) is False

        role.give_role(prof)
        assert role.is_allowed(user=prof) is True

    def test_remove_permission(self, role_model_instances, create_test_prof):
        prof = create_test_prof(num=1)
        district1, school1, club1 = role_model_instances()

        role = Role.create(district1, school1, club1)
        role.give_role(prof)

        assert role.is_allowed(user=prof) is True

        role.remove_role(prof)
        assert role.is_allowed(user=prof) is False

@pytest.fixture
def role_test_data():
    min_hier = Hierarchy.get_hierarchy(PermConst.SCHOOL_ADMIN)
    min_perms = ['modify-school']

    return min_hier, min_perms

@pytest.mark.usefixtures("perm_const_override", "db")
class TestRestPermUseExamples:
    def test_low_access_level(self, perm_const_override, create_test_prof, role_model_instances, role_test_data):
        min_hier, min_perms = role_test_data
        district1, school1, club1 = role_model_instances()
        start_model = school1

        min_role = Role.from_start_model(start_model)
        min_role.permissions.add(*min_perms)

        # Case 1 -- Lower access user tries to access higher permission level resource
        club_editor = create_test_prof(num=1)
        invalid_role = Role.create(district1, school1, club1)
        invalid_role.permissions.add('modify-club')
        invalid_role.give_role(club_editor)

        assert min_role.is_allowed(user=club_editor) is False

    def test_same_access_level(self, perm_const_override, create_test_prof, role_model_instances, role_test_data):
        min_role, min_perms = role_test_data
        district1, school1, club1 = role_model_instances()
        start_model = school1

        min_role = Role.from_start_model(start_model)
        min_role.permissions.add(*min_perms)

        # Case 2 -- Same level access with correct permission tries to access resource
        school_admin = create_test_prof(num=1)
        valid_role = Role.create(district1, school1)
        valid_role.permissions.add('modify-school', 'hide-school')
        valid_role.give_role(school_admin)

        assert min_role.is_allowed(user=school_admin) is True

    def test_same_access_level_diff_perms(self, perm_const_override, create_test_prof, role_model_instances, role_test_data):
        min_role, min_perms = role_test_data
        district1, school1, club1 = role_model_instances()
        start_model = school1

        min_role = Role.from_start_model(start_model)
        min_role.permissions.add(*min_perms)

        # Case 3 -- Same level access but does not have right permission
        school_admin = create_test_prof(num=1)
        invalid_role = Role.create(district1, school1)
        invalid_role.permissions.add('hide-school')

        assert min_role.is_allowed(user=school_admin) is False

    def test_same_access_level_diff_inst(self, perm_const_override, create_test_prof, role_model_instances, role_test_data):
        min_role, min_perms = role_test_data
        district1, school1, club1 = role_model_instances()
        start_model = school1

        min_role = Role.from_start_model(start_model)
        min_role.permissions.add(*min_perms)

        # Case 4 -- Same level access but on a different school instance
        school_admin = create_test_prof(num=1)
        district2, school2, club2 = role_model_instances()

        invalid_role = Role.create(district2, school2)
        invalid_role.permissions.add('modify-school')
        invalid_role.give_role(school_admin)

        assert min_role.is_allowed(user=school_admin) is False

    def test_higher_access_level(self, perm_const_override, create_test_prof, role_model_instances, role_test_data):
        min_role, min_perms = role_test_data
        district1, school1, club1 = role_model_instances()
        start_model = school1

        min_role = Role.from_start_model(start_model)
        min_role.permissions.add(*min_perms)

        # Case 5 -- Higher level access same school
        district_admin = create_test_prof(num=1)
        valid_role = Role.create(district1)
        valid_role.give_role(district_admin)

        assert min_role.is_allowed(user=district_admin) is True

    def test_higher_access_level_diff_inst(self, perm_const_override, create_test_prof, role_model_instances, role_test_data):
        min_role, min_perms = role_test_data
        district1, school1, club1 = role_model_instances()
        start_model = school1

        min_role = Role.from_start_model(start_model)
        min_role.permissions.add(*min_perms)

        # Case 6 -- Higher level access different district
        district_admin = create_test_prof(num=1)
        d2, s2, c1 = role_model_instances()

        invalid_role = Role.create(d2)
        invalid_role.give_role(district_admin)

        assert min_role.is_allowed(user=district_admin) is False
