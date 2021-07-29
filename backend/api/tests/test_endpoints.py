import pytest
from django.test import Client
from rest_framework.reverse import reverse
from api.serializers import *

class TestClub:
    club_get_from_code = "api:school-club-code"

    def test_retrieve_w_slug(self, client: Client, district_school_club):
        d1, s1, c1 = district_school_club()
        view_name = "api:club-detail"
        path = reverse(view_name, kwargs={'slug': c1.slug})
        retrieved = client.get(path, format="json")

        # Remove the image parameter b/c the paths are different as a result of 
        # serialization w/ and w/o request context
        data = retrieved.data
        serialized = ClubBasic(c1).data
        del data['img']
        del serialized['img']
        assert data == serialized

    
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