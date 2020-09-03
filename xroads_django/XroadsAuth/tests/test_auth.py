import pytest
from django.contrib.auth import get_user_model, authenticate
from XroadsAPI.models import *
from XroadsAuth.models import *
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from http.cookies import SimpleCookie
import datetime

class AuthRequiredViewStub(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({}, status=200)

@pytest.fixture
def setup_auth_cookies(create_test_prof):
    def func(prof_id=None, prof=None):
        if prof is None:
            assert prof_id is not None, 'Must include a prof_id if you do not provide a profile'
            prof = create_test_prof(prof_id)
        access_token = str(TokenObtainPairSerializer.get_token(prof).access_token)

        cookies = SimpleCookie()

        signature_cookie = 'JWT-SIGNATURE'
        cookies[signature_cookie] = access_token.split('.')[-1]
        cookies[signature_cookie]['HttpOnly'] = True
        cookies[signature_cookie]['SameSite'] = "Strict"
        cookies[signature_cookie]['Secure'] = True

        header_payload = 'JWT-HEADER-PAYLOAD'
        # This joins together the header and payload list items into a string
        cookies[header_payload] = '.'.join(access_token.split('.')[:2])
        cookies[header_payload]['Secure'] = True
        cookies[header_payload]['SameSite'] = "Strict"
        cookies[header_payload]['Max-Age'] = datetime.timedelta(days=7).total_seconds()

        return prof, cookies
    return func

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
    auth_required_url_name = "api:district-list"

    def test_normal_auth_request(self, create_test_prof):
        factory = APIRequestFactory()
        view = AuthRequiredViewStub.as_view()

        prof = create_test_prof(1)
        access_token = str(TokenObtainPairSerializer.get_token(prof).access_token)

        request = factory.get('', **{'HTTP_AUTHORIZATION': f"Bearer {access_token}"})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_normal_auth_invalid(self, create_test_prof):
        factory = APIRequestFactory()
        view = AuthRequiredViewStub.as_view()

        prof = create_test_prof(1)

        request = factory.get('', **{'HTTP_AUTHORIZATION': f"Bearer asdflaskdfjalsdkfj"})
        response = view(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_cookie_auth(self, setup_auth_cookies):
        prof, cookies = setup_auth_cookies(prof_id=1)

        factory = APIRequestFactory()
        factory.cookies = cookies
        view = AuthRequiredViewStub.as_view()

        request = factory.get('')
        response = view(request)

        assert response.status_code == status.HTTP_200_OK


    def test_invalid_cookie_auth(self):
        prof, cookies = setup_auth_cookies(prof_id=1)
        cookies['JWT-SIGNATURE'] = 'blahblahblah'

        factory = APIRequestFactory()
        factory.cookies = cookies
        view = AuthRequiredViewStub.as_view()

        request = factory.get('')
        response = view(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

class TestLoginView:
    def test_valid_data_cookies_set(self, setup_auth_cookies, make_request, role_model_instances, setup_client_no_auth):
        pass

    def test_invalid_data_no_cookies(self):
        pass