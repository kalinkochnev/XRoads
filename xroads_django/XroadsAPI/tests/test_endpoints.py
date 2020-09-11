import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from XroadsAuth.permissions import Role
from XroadsAPI.serializers import *
from XroadsAuth.serializers import *


# ALL views will have their authentication forced. The system used is subject to
# being changed so it will not be included here for now


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


class TestAdmin:

    class TestUserDetail:
        @pytest.fixture
        def path_other_user(self, create_test_prof):
            other_prof = create_test_prof(num=1)
            # DANGER WARNING!!!! PERIODS SCREWED UP THE REGEX FOR THE URL MATCHER
            path = reverse('api:admin-user-detail',
                           kwargs={'pk': other_prof.pk})
            return other_prof, path

        def test_get_user_no_login(self, path_other_user):
            client = APIClient()
            other_prof, path = path_other_user
            # Test error when not logged in
            response: Response = client.get(path, format='json')
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        def test_at_least_school_admin(self, role_model_instances, create_client_roles, path_other_user):
            d1, s1, c1 = role_model_instances()

            other_prof, path = path_other_user
            other_prof.join_school(s1)

            district_admin, d1_admin_role, d1_client = create_client_roles(2, [
                                                                           d1])

            school_admin, s1_admin_role, s1_client = create_client_roles(3, [
                d1, s1])
            club_editor, c1_admin_role, c1_client = create_client_roles(4, [
                                                                        d1, s1, c1])

            # Test request user must be at least a school admin to get detailed info
            response1: Response = d1_client.get(path, format='json')
            assert response1.status_code == status.HTTP_200_OK
            assert response1.data == ProfileSerializer(other_prof).data

            response2: Response = s1_client.get(path, format='json')
            assert response2.status_code == status.HTTP_200_OK

            response3: Response = c1_client.get(path, format='json')
            assert response3.status_code == status.HTTP_403_FORBIDDEN

        def test_user_doesnt_exist(self, role_model_instances, path_other_user, create_client_roles):
            d1, s1, c1 = role_model_instances()
            district_admin, d1_admin_role, d1_client = create_client_roles(2, [
                                                                           d1])

            path = reverse('api:admin-user-detail',
                           args={'lookup': 'kalin.kochnev@gmail.com'})
            response: Response = d1_client.get(path, format='json')

            assert response.status_code == status.HTTP_404_NOT_FOUND

    class TestDistrictViewset:
        retrieve_url_name = 'api:admin-district-detail'
        list_url_name = 'api:admin-district-list'

        @pytest.fixture
        def prof_w_perm(self, setup_client_auth):
            def setup(district):
                prof, client = setup_client_auth
                role = Role.from_start_model(district)
                role.give_role(prof)
                return prof, client
            return setup

        def valid_retrieve(self, client, district):
            path = reverse(self.retrieve_url_name, kwargs={'pk': district.pk})
            return client.get(path, format='json')

        def valid_list(self, client, district):
            path = reverse(self.list_url_name, kwargs={'pk': district.pk})
            return client.get(path, format='json')

        def test_no_login_retrieve(self, role_model_instances, setup_client_no_auth):
            d1, s1, c1 = role_model_instances()
            client = setup_client_no_auth
            response = self.valid_retrieve(client, d1)

            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        @pytest.mark.parametrize("method", ['post', 'delete', 'trace'])
        def test_methods_disabled_retrieve(self, method, make_request, prof_w_perm, role_model_instances):
            d1, s1, c1 = role_model_instances()
            profile, client = prof_w_perm(d1)
            path = reverse(self.retrieve_url_name, kwargs={'pk': d1.pk})
            response = make_request(client, method, path=path, format='json')

            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        @pytest.mark.parametrize("method", ['post', 'delete', 'trace'])
        def test_methods_disabled_list(self, method, make_request, prof_w_perm, role_model_instances):
            d1, s1, c1 = role_model_instances()
            user, client = prof_w_perm(d1)
            path = reverse(self.list_url_name)
            response = make_request(client, method, path=path, format='json')

            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        def test_retrieve_data(self, role_model_instances, prof_w_perm, make_request):
            d1, s1, c1 = role_model_instances()
            user, client = prof_w_perm(d1)
            path = reverse(self.retrieve_url_name, kwargs={'pk': d1.pk})
            response = make_request(client, 'get', path=path, format='json')

            expected_data = DistrictSerializer(d1).data
            assert response.data == expected_data

        def test_list_data(self, make_request, role_model_instances, prof_w_perm):
            d1, s1, c1 = role_model_instances()
            d2, s2, c2 = role_model_instances()

            user, client = prof_w_perm(d1)
            path = reverse(self.list_url_name)
            response = make_request(client, 'get', path=path, format='json')

            expected_data = DistrictSerializer([d1, d2], many=True).data

            assert response.data == expected_data

        def test_does_not_exist(self, setup_client_auth, make_request):
            user, client = setup_client_auth
            path = reverse(self.retrieve_url_name, args={'pk': 1})
            response = make_request(client, 'get', path=path, format='json')
            assert response.status_code == status.HTTP_404_NOT_FOUND

    class TestSchoolViewset:
        # GET and LIST cannot be easily tested because the img url is different since the response is from a view
        retrieve_url_name = 'api:admin-school-detail'
        list_url_name = 'api:admin-school-list'

        @pytest.fixture
        def prof_w_perm(self, setup_client_auth):
            def setup(school):
                prof, client = setup_client_auth
                role = Role.from_start_model(school)
                role.give_role(prof)
                return prof, client
            return setup

        def valid_retrieve(self, client, school):
            path = reverse(self.retrieve_url_name, kwargs={
                           'district_pk': school.district.id, 'pk': school.pk})
            return client.get(path, format='json')

        def valid_list(self, client, school):
            path = reverse(self.list_url_name, kwargs={
                           'district_pk': school.district.id, 'pk': school.pk})
            return client.get(path, format='json')

        def test_no_login_retrieve(self, role_model_instances, setup_client_no_auth):
            d1, s1, c1 = role_model_instances()
            client = setup_client_no_auth
            response = self.valid_retrieve(client, s1)

            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        @pytest.mark.parametrize("method", ['post', 'delete', 'trace'])
        def test_methods_disabled_retrieve(self, method, make_request, prof_w_perm, role_model_instances):
            d1, s1, c1 = role_model_instances()
            profile, client = prof_w_perm(s1)
            path = reverse(self.retrieve_url_name, kwargs={
                           'district_pk': s1.district.id, 'pk': s1.pk})
            response = make_request(client, method, path=path, format='json')

            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        @pytest.mark.parametrize("method", ['post', 'delete', 'trace'])
        def test_methods_disabled_list(self, method, make_request, prof_w_perm, role_model_instances):
            d1, s1, c1 = role_model_instances()
            user, client = prof_w_perm(s1)
            path = reverse(self.list_url_name, kwargs={
                           'district_pk': s1.district.id})
            response = make_request(client, method, path=path, format='json')

            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        def test_does_not_exist(self, setup_client_auth, make_request):
            d1 = District.objects.create(name='d1')

            user, client = setup_client_auth
            path = reverse(self.retrieve_url_name, args={
                           'district_pk': d1.id, 'pk': 1})
            response = make_request(client, 'get', path=path, format='json')
            assert response.status_code == status.HTTP_404_NOT_FOUND

    class TestClubViewset:
        # GET and LIST cannot be easily tested because the img field screws things up
        retrieve_url_name = 'api:admin-club-detail'
        toggle_hide_url_name = 'api:admin-club-toggle-hide'

        @pytest.fixture
        def prof_w_perm(self, setup_client_auth):
            def setup(club):
                prof, client = setup_client_auth
                role = Role.from_start_model(club)
                role.give_role(prof)
                return prof, client
            return setup

        def valid_retrieve(self, client, club):
            path = reverse(self.retrieve_url_name, kwargs={
                           'district_pk': club.district.id, 'school_pk': club.school.pk, 'pk': club.pk})
            return client.get(path, format='json')

        def test_no_login_retrieve(self, role_model_instances, setup_client_no_auth):
            d1, s1, c1 = role_model_instances()
            client = setup_client_no_auth
            response = self.valid_retrieve(client, c1)

            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        @pytest.mark.parametrize("method", ['post', 'delete', 'trace'])
        def test_methods_disabled_retrieve(self, method, make_request, prof_w_perm, role_model_instances):
            d1, s1, c1 = role_model_instances()
            profile, client = prof_w_perm(s1)
            path = reverse(self.retrieve_url_name, kwargs={
                           'district_pk': c1.district.id, 'school_pk': c1.school.pk, 'pk': c1.pk})
            response = make_request(client, method, path=path, format='json')

            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        def test_does_not_exist(self, setup_client_auth, make_request, role_model_instances):
            d1, s1, c1 = role_model_instances()
            c1.delete()

            user, client = setup_client_auth
            path = reverse(self.retrieve_url_name, args={
                           'district_pk': c1.district.id, 'school_pk': c1.school.pk, 'pk': 1})
            response = make_request(client, 'get', path=path, format='json')
            assert response.status_code == status.HTTP_404_NOT_FOUND

        def test_toggle_hide(self, prof_w_perm, make_request, role_model_instances):
            d1, s1, c1 = role_model_instances()
            assert c1.is_visible is False

            profile, client = prof_w_perm(c1)
            path = reverse(self.toggle_hide_url_name, kwargs={'district_pk': c1.district.id, 'school_pk': c1.school.pk, 'pk': c1.pk})
            response = make_request(client, 'post', path=path, format='json')

            assert response.status_code == status.HTTP_202_ACCEPTED
            assert c1.is_visible is True
            

class TestNoAuth:
    class TestClubViewset:
        club_path_name = "api:club-list"

        def test_retrieves_club_list_no_auth(self, role_model_instances, make_request, setup_client_no_auth):
            d1, s1, c1 = role_model_instances()
            client = setup_client_no_auth
            path = reverse(self.club_path_name, kwargs={
                           'district_pk': d1.id, 'school_pk': s1.id})
            response: Response = make_request(
                client, 'get', path=path, format='json')

            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        def test_retrieves_club_list_w_auth(self, role_model_instances, make_request, setup_client_auth, create_club):
            d1, s1, c1 = role_model_instances()
            for i in range(c1.id+1, c1.id+4):
                club = create_club(id=i)
                s1.add_club(club, save=False)
            s1.make_save(save=True)

            profile, client = setup_client_auth
            path = reverse(self.club_path_name, kwargs={
                           'district_pk': d1.id, 'school_pk': s1.id})
            response: Response = make_request(
                client, 'get', path=path, format='json')

            assert response.status_code == status.HTTP_200_OK
            assert response.data == BasicClubInfoSerial(
                s1.clubs, many=True).data
