import pytest
from django.test import Client
from rest_framework.reverse import reverse
from api.serializers import *

class TestClub:

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