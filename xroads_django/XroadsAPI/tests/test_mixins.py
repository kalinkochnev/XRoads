from XroadsAPI.mixins import *
import pytest
from rest_framework.test import APIRequestFactory
from unittest.mock import MagicMock

class RequestStub:
    def __init__(self, data):
        self.data = data

class DummyAddAdmin(AddAdminMixin):
    def __init__(self, object):
        self.object = object
        super().__init__()

    def get_object(self):
        return self.object

class TestAddAdminMixin:
    def test_add_admin_request(self, create_test_prof):
        factory = APIRequestFactory()

        d1 = District.objects.create(name='d1')
        profiles = [create_test_prof(i) for i in range(5)]
        add_mixin = DummyAddAdmin(d1)
        permissions = ['modify-district']

        # Expected allowed access
        role = Role.from_start_model(d1)
        role.permissions.add(*permissions)

        for prof in profiles:
            assert role.is_allowed(user=prof) is False

        data = {
            'emails': [p.email for p in profiles],
            'permissions': permissions,
        }

        response = add_mixin.add_admins(RequestStub(data), hier_role=PermConst.DISTRICT_ADMIN)

        for prof in profiles:
            assert role.is_allowed(user=prof) is True

        assert response.status_code == status.HTTP_202_ACCEPTED
    
    def test_send_invalid_data(self, create_test_prof):
        factory = APIRequestFactory()

        d1 = District.objects.create(name='d1')
        profiles = [create_test_prof(i) for i in range(5)]
        add_mixin = DummyAddAdmin(d1)
        permissions = ['modify-district']

        # Expected allowed access
        role = Role.from_start_model(d1)
        role.permissions.add(*permissions)

        for prof in profiles:
            assert role.is_allowed(user=prof) is False

        data = {
            'emails': ['asdfasdf', 'asdfsadf', 'asdfasdfsdaf'],
            'permissions': permissions,
        }

        response = add_mixin.add_admins(RequestStub(data), hier_role=PermConst.DISTRICT_ADMIN)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    

class TestRemoveAdminMixin:
    def valid_post_request(self):
        pass