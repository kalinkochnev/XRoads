import pytest

import XroadsAuth.permisson_constants as PermConst
from XroadsAPI.forms import *


@pytest.fixture
def profiles_data(create_test_prof):
    return [create_test_prof(i) for i in range(3)]


class TestUserEmailForm:
    def test_invalid_when_account_doesnt_exist(self, create_test_prof):
        emails = [f'email{i}@email.com' for i in range(3)]
        assert EmailListForm(data={'profile_emails': emails}).is_valid() is False

    def test_valid_when_account_exists(self, create_test_prof, profiles_data):
        profiles = profiles_data
        emails = [p.email for p in profiles] 

        assert EmailListForm(data={'emails': emails}).is_valid() is True

    def test_profiles_attr(self, create_test_prof, profiles_data):
        profiles = profiles_data
        fake_emails = [f'email{i}@email.com' for i in range(3, 5)]
        emails = [p.email for p in profiles] + fake_emails

        email_form = EmailListForm(data={'emails': emails})
        email_form.is_valid()
        profiles, non_existant_emails = email_form.profiles

        assert profiles == profiles
        assert fake_emails == non_existant_emails


class TestAdminRoleForm:
    def test_valid_form(self, perm_const_override, create_test_prof):
        prof = create_test_prof(1)
        permissions = ['add-admin', 'modify-club']

        data = {
            'permissions': permissions,
            'email': prof.email
        }


        form = AddAdminForm(hier_role=PermConst.CLUB_EDITOR, data=data)

        assert form.is_valid() is True
        assert form.validated_data['permissions'] == permissions

    def test_invalid_perms_given(self, perm_const_override, create_test_prof):
        prof = create_test_prof(1)

        data = {
            'permissions': ['create-school', 'modify-district'],
            'emails': prof.email
        }

        assert AddAdminForm(hier_role=PermConst.CLUB_EDITOR, data=data).is_valid() is False

    def test_user_no_exist(self, perm_const_override):
        data = {
            'permissions': ['create-school', 'modify-district'],
            'emails': 'random@email.com'
        }

        assert AddAdminForm(hier_role=PermConst.CLUB_EDITOR, data=data).is_valid() is False