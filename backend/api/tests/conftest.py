import tempfile
from typing import Callable, Dict, Optional

import pytest
from api.models import *
from django.http.response import HttpResponse
from django.test import override_settings
from django.test.client import Client
from PIL import Image
from rest_framework.test import APIClient


@pytest.fixture
def temp_img():
    def get_temp_img(temp_file):
        size = (200, 200)
        color = (255, 0, 0, 0)
        image = Image.new("RGB", size, color)
        image.save(temp_file, 'jpeg')
        return temp_file
    return get_temp_img


@pytest.fixture
def create_club(db, temp_img):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def create_club(club_id=-1, **kwargs):
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")

        data = {
            'name': "Test Club",
            'description': "This is a club description",
            'presentation_url': "https://docs.google.com/presentation/d/fake_id/edit",
            'code': 'Random52Code23',
            'slug': 'test-slug',
            'is_visible': True,
            'img': temp_img(temp_file).name,
        }
        data.update(kwargs)

        club = None
        if club_id == -1:
            club = Club.objects.create(**data)
        else:
            club = Club.objects.create(id=club_id, **data)

        # Makes sure it is unique
        club.slug += str(club.id)
        club.save()

        return club

    return create_club


@pytest.fixture
def district_school_club(db, create_club):
    def create(club_data={}):
        district1 = District.objects.create(name="d1")
        school1 = School.objects.create(name="s1")
        club1 = create_club(**club_data)

        district1.add_school(school1)
        school1.add_club(club1)

        return (district1, school1, club1)
    return create


@pytest.fixture
def make_request():
    def make(client: Client, method: str, path: str, format: str = 'json', *args, **kwargs) -> HttpResponse:
        method_map: Dict[str, Callable] = {
            'get': client.get,
            'post': client.post,
            'put': client.put,
            'patch': client.patch,
            'delete': client.delete,
            'head': client.head,
            'options': client.options,
            'trace': client.trace,
        }
        return method_map[method](path=path, format=format, *args, **kwargs)
    return make
