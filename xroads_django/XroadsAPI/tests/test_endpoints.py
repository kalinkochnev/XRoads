import tempfile

from django.urls.base import reverse
from testutils.conftest import create_club, make_request
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from XroadsAPI.serializers import *


class TestClub:
    club_get_from_code = "api:school-club-code"

    def test_club_code_valid_get(self, setup_client_no_auth, make_request, role_model_instances):
        code = "Random24Code"
        d1, s1, c1 = role_model_instances(club_data={'code': code})
        client = setup_client_no_auth()
        path = reverse(self.club_get_from_code, kwargs={'pk': s1.id})
        request_data = {'code': code}

        response = make_request(client, 'get', data=request_data, path=path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == BasicClubInfoSerial(c1).data

    def test_club_code_invalid_get(self, setup_client_no_auth, make_request, role_model_instances):
        d1, s1, c1 = role_model_instances(club_data={'code': 'randomCode'})
        client = setup_client_no_auth()
        path = reverse(self.club_get_from_code, kwargs={'pk': s1.id})
        request_data = {
            'code': 'bad_code',
        }

        response = make_request(client, 'get', data=request_data, path=path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
