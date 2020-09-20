from rest_framework.test import APIRequestFactory

from XroadsAPI.mixins import *


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
    def test_add_admin_request(self, create_test_prof, perm_const_override):
        factory = APIRequestFactory()

        d1 = District.objects.create(name='d1')
        prof = create_test_prof(1)
        add_mixin = DummyAddAdmin(d1)
        permissions = ['modify-district']

        # Expected allowed access
        role = Role.from_start_model(d1)
        role.permissions.add(*permissions)

        assert role.is_allowed(user=prof) is False

        data = {
            'email': prof.email,
            'permissions': permissions,
        }

        response = add_mixin.add_admin(RequestStub(
            data), hier_role=PermConst.DISTRICT_ADMIN)


        assert response.status_code == status.HTTP_202_ACCEPTED
        assert role.is_allowed(user=prof) is True

    def test_send_invalid_data(self, create_test_prof, perm_const_override):
        factory = APIRequestFactory()

        d1 = District.objects.create(name='d1')
        add_mixin = DummyAddAdmin(d1)

        data = {
            'emails': 'asdfasdf',
            'permissions': permissions,
        }

        response = add_mixin.add_admin(RequestStub(
            data), hier_role=PermConst.DISTRICT_ADMIN)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class DummyRemoveAdmin(RemoveAdminMixin):
    def __init__(self, object):
        self.object = object
        super().__init__()

    def get_object(self):
        return self.object


class TestRemoveAdminMixin:
    def test_remove_admin_request(self, create_test_prof, perm_const_override):
        factory = APIRequestFactory()

        d1 = District.objects.create(name='d1')
        prof = create_test_prof(1)
        add_mixin = DummyRemoveAdmin(d1)
        permissions = ['modify-district']

        # Expected allowed access
        role = Role.from_start_model(d1)
        role.permissions.add(*permissions)
        role.give_role(prof)

        assert role.is_allowed(user=prof) is True

        data = {
            'email': prof.email,
        }

        response = add_mixin.remove_admin(RequestStub(data))

        assert role.is_allowed(user=prof) is False

        assert response.status_code == status.HTTP_202_ACCEPTED

    def test_send_invalid_data(self, create_test_prof, perm_const_override):
        factory = APIRequestFactory()

        d1 = District.objects.create(name='d1')
        add_mixin = DummyRemoveAdmin(d1)

        data = {
            'emails': 'blahalksdjf',
        }

        response = add_mixin.remove_admin(RequestStub(data))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
