import pytest
from rest_framework import serializers
from XroadsAPI.forms import UserEmailForm
import XroadsAPI.permisson_constants as PermConst

class TestUserEmailForm:
    def test_invalid_when_account_doesnt_exist(self, create_test_prof):
        emails = [f'email{i}@email.com' for i in range(10)]
        assert UserEmailForm(data={'profile_emails': emails}).is_valid() is False

    def test_valid_when_account_exists(self, create_test_prof):
        profiles = [create_test_prof(i) for i in range(10)]
        emails = [p.email for p in profiles] 

        assert UserEmailForm(data={'emails': emails}).is_valid() is True

    def test_profiles_attr(self, create_test_prof):
        profiles = [create_test_prof(i) for i in range(10)]
        fake_emails = [f'email{i}@email.com' for i in range(20, 30)]
        emails = [p.email for p in profiles] + fake_emails

        email_form = UserEmailForm(data={'emails': emails})
        email_form.is_valid()
        profiles, non_existant_emails = email_form.profiles

        assert profiles == profiles
        assert fake_emails == non_existant_emails


    