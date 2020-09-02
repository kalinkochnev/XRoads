import pytest
from django.contrib.auth import get_user_model, authenticate
from XroadsAPI.models import *
from XroadsAuth.models import *

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