import pytest

from XroadsAuth.permissions import Role
from XroadsAuth.models import RoleModel
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
            'school': None,
            'district': None,
            'permissions': [],
            'joined_clubs': [],  
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
            'school': None,
            'district': None,
            'permissions': [],
            'joined_clubs': [],
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
            'school': None,
            'district': None,
            'is_anon': prof.is_anon,
            'permissions': [
                f'Club-{c1.id}/perms=[add-admin, modify-club]',
                f'School-{s1.id}/perms=[__all__]',
            ],
            'joined_clubs': [],
        }

        assert ProfileSerializer(prof).data == expected

    def test_district_school_set(self, role_model_instances, create_test_prof):
        d1, s1, c1 = role_model_instances()
        
        prof = create_test_prof(1)
        prof.join_school(s1)
        prof.district = d1
        prof.save()

        expected = {
            'id': prof.id,
            'email': prof.email,
            'first_name': prof.first_name,
            'last_name': prof.last_name,
            'school': s1.id,
            'district': d1.id,
            'is_anon': prof.is_anon,
            'permissions': [],
            'joined_clubs': [],
        }

        assert ProfileSerializer(prof).data == expected

    def test_joined_clubs(self, role_model_instances, create_test_prof, create_club):
        d1, s1, c1 = role_model_instances()
        c2 = create_club()
        prof = create_test_prof(1)

        c1.join(prof)
        c2.join(prof)

        expected = OrderedDict({
            'id': prof.id,
            'email': prof.email,
            'first_name': prof.first_name,
            'last_name': prof.last_name,
            'school': None,
            'district': None,
            'is_anon': prof.is_anon,
            'permissions': [],
            'joined_clubs': [c1.id, c2.id],
        })

        assert dict(OrderedDict(ProfileSerializer(prof).data)) == dict(expected)



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

        hier_perm = RoleModel.get_role(role)
        assert hier_perm.highest_level_str == f'School-{school1.id}/perms=[create-club]'

class TestEditorSerializer:
    def test_valid_data(self, perm_const_override, create_test_prof, role_model_instances):
        d1, s1, c1 = role_model_instances()
        
        role = Role.from_start_model(c1)
        role.permissions.add('hide-club')

        prof = create_test_prof(1)
        role.give_role(prof)
        serializer = EditorSerializer(prof, context={'role': role})
        
        expected_data = {
            'profile': {
                'id': prof.id,
                'email': prof.email,
                'first_name': prof.first_name,
                'last_name': prof.last_name,
            },
            'perms': ['hide-club']
        }

        assert serializer.data == expected_data