from rest_framework.test import APIClient
import pytest
from XroadsAuth.models import Profile
from django.urls import reverse
from rest_framework.response import Response
from XroadsAPI.permissions import Role, Permissions, Hierarchy
# ALL views will have their authentication forced. The system used is subject to
# being changed so it will not be included here for now
@pytest.fixture
def setup_client_no_auth(create_test_prof):
    profile = create_test_prof(id=1)
    client = APIClient()
    client.force_authenticate(user=profile)

    return profile, client


@pytest.fixture
def setup_client_auth(setup_client_no_auth):
    profile, client = setup_client_no_auth
    client.force_authenticate(user=profile)

    return profile, client


class AdminGeneralViews:
    def test_get_user(self, setup_client_no_auth, create_test_prof):
        request_prof, client = setup_client
        client: APIClient = client
        other_prof = create_test_prof(id=2)

        path = reverse('admin-get-profile', kwargs={'email': other_prof.email})

        # Test error when logged out
        client.logout()
        response: Response = client.post(path, format='json')
        assert response.status_code == 401

    def test_at_least_school_admin(self):
        other_prof = create_test_prof(id=2)
        other_prof.join_school(school)

        d1 = District.objects.create(name='d')
        s1 = School.objects.create(name='s')
        d1.add_school(s1)
        c1 = create_club(id=1)
        s1.add_club(c1)

        district_admin = create_test_prof(id=3)
        d1_admin_role = Role.create(d1)
        d1_admin_role.give_role(district_admin)
        d1_client = APIClient()
        d1_client.force_authenticate(user=district_admin)

        school_admin = create_test_prof(id=4)
        s1_admin_role = Role.create(d1, s1)
        s1_admin_role.give_role(school_admin)
        s1_client = APIClient()
        s1_client.force_authenticate(user=school_admin)

        club_editor = create_test_prof(id=5)
        c1_admin_role = Role.create(d1, s1, c1)
        c1_admin_role.give_role(school_admin)
        c1_client = APIClient()
        c1_client.force_authenticate(user=club_editor)

        # Test request user must be at least a school admin to get detailed info
        path = reverse('admin-get-profile', kwargs={'email': other_prof.email})
        
        response1: Response = d1_client.post(path, format='json')
        assert response1.status_code == 200

        response2: Response = s1_client.post(path, format='json')
        assert response2.status_code == 200

        response3: Response = c1_client.post(path, format='json')
        assert response3.status_code == 401


    @pytest.mark.parametrize('permissions, expected', [
        [['__all__'], 200],
        [['modify-school'], 200],
        [['create-club'], 200],
        [['create-club', 'modify-school'], 200],
        [['hide-school', 401]],
        [['blah blah blah', 401]],

    ])
    def test_get_user_school_admin_perm_test(self, permissions, expected, setup_client_auth, create_test_prof):
        request_prof, client = setup_client

        other_prof = create_test_prof(id=2)
        school = School.objects.create(name='s')
        other_prof.join_school(school)

        role = Role.from_start_model(school)    
        role.permissions.add(*permissions)
        role.give_role(request_prof)

        path = reverse('admin-get-profile', kwargs={'email': other_prof.email})
        response: Response = client.post(path, format='json')

        assert response.status_code == expected


    def test_get_self_info(self):
        pass


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
