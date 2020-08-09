import pytest
from rest_framework.test import APIClient
from XroadsAuth.models import Profile
from django.urls import reverse
from rest_framework.response import Response
from XroadsAPI.permissions import Role, Permissions, Hierarchy
# ALL views will have their authentication forced. The system used is subject to
# being changed so it will not be included here for now


@pytest.fixture
def setup_client_no_auth(create_test_prof):
    profile = create_test_prof(num=1)
    client = APIClient()
    client.force_authenticate(user=profile)

    return profile, client


@pytest.fixture
def setup_client_auth(setup_client_no_auth):
    profile, client = setup_client_no_auth
    client.force_authenticate(user=profile)

    return profile, client


@pytest.fixture
def create_client_roles(create_test_prof):
    def create(prof_id, role_objs, is_auth=True, perms=['__all__']):
        prof = create_test_prof(num=prof_id)
        role = Role.create(*role_objs)
        role.permissions.add(*perms)
        role.give_role(prof)

        client = APIClient()
        if is_auth:
            client.force_authenticate(user=prof)
        return prof, role, client
    return create


@pytest.fixture
def path_other_user(create_test_prof):
    other_prof = create_test_prof(num=1)
    # DANGER WARNING!!!! PERIODS SCREWED UP THE REGEX FOR THE URL MATCHER
    path = reverse('user-admin-detail', kwargs={'pk': other_prof.pk})
    return other_prof, path


class TestAdminGeneralViews:
    def test_get_user_no_login(self, path_other_user):
        client = APIClient()
        other_prof, path = path_other_user
        # Test error when not logged in
        response: Response = client.get(path, format='json')
        assert response.status_code == 403

    def test_at_least_school_admin(self, role_model_instances, create_client_roles, path_other_user):
        d1, s1, c1 = role_model_instances()

        other_prof, path = path_other_user
        other_prof.join_school(s1)

        district_admin, d1_admin_role, d1_client = create_client_roles(2, [d1])
        
        school_admin, s1_admin_role, s1_client = create_client_roles(3, [
                                                                     d1, s1])
        club_editor, c1_admin_role, c1_client = create_client_roles(4, [
                                                                    d1, s1, c1])

        # Test request user must be at least a school admin to get detailed info
        response1: Response = d1_client.get(path, format='json')
        assert response1.status_code == 200

        response2: Response = s1_client.get(path, format='json')
        assert response2.status_code == 200

        response3: Response = c1_client.get(path, format='json')
        assert response3.status_code == 403

    @pytest.mark.parametrize('permissions, expected', [
        [['__all__'], 200],
        [['view-user-detail'], 200],
        [['create-club'], 403],
        [['create-club', 'modify-school'], 403],
        # [['blah blah blah'], 401], add test that checks for a random string (doesn't work cause of assert statement in Role)

    ])
    def test_get_user_school_admin_perm_test(self, permissions, expected, role_model_instances, create_client_roles, path_other_user):
        d1, s1, c1 = role_model_instances()

        other_prof, path = path_other_user
        other_prof.join_school(s1)

        school_admin, s1_admin_role, s1_client = create_client_roles(2, [d1, s1], perms=permissions)

        response: Response = s1_client.get(path, format='json')

        assert response.status_code == expected

    def test_get_user_district_admin_no_perms(self, role_model_instances, create_client_roles, path_other_user):
        d1, s1, c1 = role_model_instances()

        other_prof, path = path_other_user
        other_prof.join_school(s1)

        district_admin, d1_admin_role, d1_client = create_client_roles(2, [d1])

        response: Response = d1_client.get(path, format='json')

        assert response.status_code == 200

    def test_get_user_not_in_school_not_allowed(self, role_model_instances, path_other_user, create_client_roles):
        d1, s1, c1 = role_model_instances()
        d2, s2, c2 = role_model_instances()

        other_prof, path = path_other_user
        other_prof.join_school(s2)

        district_admin, d1_admin_role, d1_client = create_client_roles(2, [d1])
        school_admin, s1_admin_role, s1_client = create_client_roles(3, [d1, s1])

        response: Response = d1_client.get(path, format='json')

        assert response.status_code == 403

    def test_user_doesnt_exist(self, role_model_instances, path_other_user, create_client_roles):
        d1, s1, c1 = role_model_instances()
        district_admin, d1_admin_role, d1_client = create_client_roles(2, [d1])

        path = reverse('user-admin-detail', args={'lookup': 'kalin.kochnev@gmail.com'})
        response: Response = d1_client.get(path, format='json')

        assert response.status_code == 404


class ClubEditorViews:

    def test_add_editor(self):
        pass

    def test_remove_editor(self):
        pass

    def test_modify_club(self):
        pass

    def test_create_club_not_allowed(self):
        pass


class SchoolAdminViews:
    def test_create_club_allowed(self):
        pass

    def test_create_school_not_allowed(self):
        pass


class DistrictAdminViews:
    pass
