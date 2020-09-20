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

        expected_response = EditorSerializer(prof, context={'role': role}).data

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.data == expected_response
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


class DummyListAdmin(ListAdminMixin):
    def __init__(self, object):
        self.object = object
        super().__init__()

    def get_object(self):
        return self.object


class TestListAdminMixin:
    def test_get_admins(self, role_model_instances, perm_const_override, create_test_prof):
        d1, s1, c1 = role_model_instances()
        profs = [create_test_prof(i) for i in range(3)]
        dummy_list = DummyListAdmin(c1)

        r1 = Role.from_start_model(c1)
        r1.permissions.add('hide-club')
        r1.give_role(profs[0])

        r2 = Role.from_start_model(c1)
        r2.permissions.add('add-admin')
        r2.give_role(profs[1])

        unrelated_role = Role.from_start_model(s1)
        unrelated_role.give_role(profs[2])

        expected_data = {
            'poss_perms': r1.hierarchy.poss_perms,
            'admins': [
                {
                    'profile': {
                        'id': profs[0].id,
                        'email': profs[0].email,
                        'first_name': profs[0].first_name,
                        'last_name': profs[0].last_name
                    },
                    'perms': ['hide-club']
                },
                {
                    'profile': {
                        'id': profs[1].id,
                        'email': profs[1].email,
                        'first_name': profs[1].first_name,
                        'last_name': profs[1].last_name
                    },
                    'perms': ['add-admin']
                },
            ]
        }

        response = dummy_list.list_admins(RequestStub({}))
        assert response.data == expected_data
