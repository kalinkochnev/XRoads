import pytest

from XroadsAuth.permissions import Role
from XroadsAuth.models import HierarchyPerms
from XroadsAuth.serializers import *
from collections import OrderedDict

class TestProfileSerializers:
    def test_profile_serialization(self, db):
        user_obj: Profile = Profile.objects.create_user(
            email="a@email.com", password="password", first_name="a", last_name="b", is_anon=True)
        expected = {
            'id': user_obj.id,
            'email': user_obj.email,
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name,
            'is_anon': user_obj.is_anon,
            'permissions': [],
        }

        assert expected == ProfileSerializer(user_obj).data


    def test_profile_optional_fields(self, db):
        user_obj = Profile.objects.create_user(
            email="a@email.com", password="password", first_name="a", last_name="b")
        expected = {
            'id': user_obj.id,
            'email': user_obj.email,
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name,
            'is_anon': user_obj.is_anon,
            'permissions': [],
        }

        assert expected == ProfileSerializer(user_obj).data


    def test_profile_from_dict(self, db):
        user_obj: Profile = Profile(email="a@email.com", password="password",
                                    first_name="a", last_name="b",is_anon=True)
        data = OrderedDict({
            'email': user_obj.email,
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name,
            'is_anon': user_obj.is_anon,
        })

        serializer = ProfileSerializer(data=data)
        serializer.is_valid()
        result: Profile = serializer.save()

        assert result.email == user_obj.email
        assert result.first_name == user_obj.first_name
        assert result.last_name == user_obj.last_name
        assert result.is_anon == user_obj.is_anon

    def test_profile_serialize_permissions(self, db, role_model_instances, perm_const_override, create_test_prof):
        d1, s1, c1 = role_model_instances()
        prof = create_test_prof(1)

        role = Role.from_start_model(c1)
        role.permissions.add('modify-club', 'add-admin')
        role.give_role(prof)

        role = Role.from_start_model(s1)
        role.permissions.allow_all_perms()
        role.give_role(prof)

        expected = {
            'id': prof.id,
            'email': prof.email,
            'first_name': prof.first_name,
            'last_name': prof.last_name,
            'is_anon': prof.is_anon,
            'permissions': [
                f'District-{d1.id}/School-{s1.id}/Club-{c1.id}/perms=[add-admin, modify-club]',
                f'District-{d1.id}/School-{s1.id}/perms=[__all__]',
            ]
        }

        assert ProfileSerializer(prof).data == expected


class TestAnonProfileSerializers:
    @pytest.fixture
    def gen_profiles(self, db, create_test_prof):
        def gen_profiles(num):
            visible = []
            invisible = []
            for i in range(num):
                if i % 2 == 0:
                    visible.append(create_test_prof(num))
                else:
                    invisible.append(create_test_prof(num))
            return visible, invisible


    def test_anon_profile_remove_anon(self, db, gen_profiles, create_test_prof):
        prof1 = create_test_prof(1, is_anon=True)
        expected = {
            'is_anon': True
        }

        assert AnonProfileSerializer(prof1).data == expected


    def test_anon_prof_not_anon_serialization(self, db, create_test_prof):
        prof1 = create_test_prof(1)
        expected = {
            'id': prof1.id,
            'email': prof1.email,
            'first_name': prof1.first_name,
            'last_name': prof1.last_name,
            'is_anon': prof1.is_anon,
        }

        assert AnonProfileSerializer(prof1).data == expected



class TestPermissionSerializer:
    def test_highest_level_str(self, perm_const_override, create_test_prof, role_model_instances):
        prof = create_test_prof(1)
        district1, school1, club1 = role_model_instances()

        role = Role.from_start_model(school1)
        role.permissions.add('create-club')
        role.give_role(prof)

        hier_perm = HierarchyPerms.objects.get(perm_name=str(role))
        assert hier_perm.highest_level_str == 'School-1/perms=[create-club]'

    def test_serialize_permission(self, perm_const_override, create_test_prof, role_model_instances):
        prof = create_test_prof(1)
        district1, school1, club1 = role_model_instances()

        role1 = Role.from_start_model(club1)
        role1.give_role(prof)
        hier_perm = HierarchyPerms.objects.get(perm_name=str(role1))

        
        """role2 = Role.from_start_model(school1)
        role1.give_role(prof)
        role3 = Role.from_start_model(district1)
        role1.give_role(prof)
        expected = [i.highest_level_str for i in prof.hierarchy_perms]"""

        expected = hier_perm.highest_level_str
        # assert expected == PermissionSerializer(hier_perm).data