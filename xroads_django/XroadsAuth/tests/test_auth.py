import pytest
from django.contrib.auth import get_user_model, authenticate
from XroadsAPI.models import *
from XroadsAuth.models import *

class TestRegistration:
    url = "/auth/registration/"
    def test_valid(self, role_model_instances, setup_client_no_auth, make_request):
        d1, s1, c1 = role_model_instances()
        d1.add_email_domain('niskyschools.org')
        client = setup_client_no_auth

        data = {
            'email': 'test@niskyschools.org',
            'first_name': 'test_first',
            'last_name': 'test_last',
            'password1': '32984kjwdss',
            'password2': '32984kjwdss',
        }

        # path = reverse(self.url)
        response = make_request(client, 'post', path=self.url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_exists(self, role_model_instances, setup_client_no_auth, make_request):
        d1, s1, c1 = role_model_instances()
        d1.add_email_domain('niskyschools.org')
        
        prof = Profile.objects.create_user(email="test@niskyschools.org", password='23kj2k3sd')
        
        client = setup_client_no_auth

        data = {
            'email': prof.email,
            'first_name': 'test_first',
            'last_name': 'test_last',
            'password1': '32984kjwdss',
            'password2': '32984kjwdss',
        }

        # path = reverse(self.url)
        response = make_request(client, 'post', path=self.url, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_district_not_existing(self, role_model_instances, setup_client_no_auth, make_request):
        d1, s1, c1 = role_model_instances()
        d1.add_email_domain('niskyschools.org')
        
        client = setup_client_no_auth

        data = {
            'email': "test@sdflkjsdklf.com",
            'first_name': 'test_first',
            'last_name': 'test_last',
            'password1': '32984kjwdss',
            'password2': '32984kjwdss',
        }

        # path = reverse(self.url)
        response = make_request(client, 'post', path=self.url, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

class TestAuthenticatedRequest:
    def test_normal_auth_request(self):
        pass

    def test_cookie_auth(self):
        pass

    def test_invalid_cookie_auth(self):
        pass

class TestLoginView:
    def test_valid_data_cookies_set(self):
        pass

    def test_invalid_data_no_cookies(self):
        pass