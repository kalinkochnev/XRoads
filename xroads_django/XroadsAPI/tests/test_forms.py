import pytest
from rest_framework import serializers
from XroadsAPI.forms import *
import XroadsAPI.permisson_constants as PermConst

@pytest.fixture
def profiles_data(create_test_prof):
    return [create_test_prof(i) for i in range(3)]


class TestUserEmailForm:
    def test_invalid_when_account_doesnt_exist(self, create_test_prof):
        emails = [f'email{i}@email.com' for i in range(3)]
        assert UserEmailForm(data={'profile_emails': emails}).is_valid() is False

    def test_valid_when_account_exists(self, create_test_prof, profiles_data):
        profiles = profiles_data
        emails = [p.email for p in profiles] 

        assert UserEmailForm(data={'emails': emails}).is_valid() is True

    def test_profiles_attr(self, create_test_prof, profiles_data):
        profiles = profiles_data
        fake_emails = [f'email{i}@email.com' for i in range(3, 5)]
        emails = [p.email for p in profiles] + fake_emails

        email_form = UserEmailForm(data={'emails': emails})
        email_form.is_valid()
        profiles, non_existant_emails = email_form.profiles

        assert profiles == profiles
        assert fake_emails == non_existant_emails


class TestAdminRoleForm:
    def test_valid_form(self, perm_const_override, create_test_prof, profiles_data):
        profiles = profiles_data
        permissions = ['add-admin', 'modify-club']

        data = {
            'permissions': permissions,
            'emails': [p.email for p in profiles]
        }


        form = AdminRoleForm(hier_role=PermConst.CLUB_EDITOR, data=data)

        assert form.is_valid() is True
        assert form.validated_data['permissions'] == permissions

    def test_invalid_perms_given(self, perm_const_override, create_test_prof, profiles_data):
        profiles = profiles_data

        data = {
            'permissions': ['create-school', 'modify-district'],
            'emails': [p.email for p in profiles]
        }

        assert AdminRoleForm(hier_role=PermConst.CLUB_EDITOR, data=data).is_valid() is False
