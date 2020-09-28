import pytest
from rest_framework.reverse import reverse
from XroadsAuth.serializers import ProfileSerializer

class TestUserDetailView:
    def test_correct_serializer_used(self, setup_client_auth, make_request):
        prof, client = setup_client_auth()
        url = reverse('rest_user_details')

        response = make_request(client, 'get', path=url, format='json')

        assert response.data == ProfileSerializer(prof).data
