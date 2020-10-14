import pytest
from django.test import override_settings
from XroadsAPI.models import *
import tempfile
from PIL import Image
from XroadsAPI.slide import SlideTemplates
from rest_framework.test import APIClient

@pytest.fixture
def setup_client_no_auth():
    def setup():
        client = APIClient()
        return client
    return setup


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
    def create_club(id=-1):
        name = "Test Club"
        description = "This is a club description"
        commitment = "7hrs/week"
        is_visible = False

        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        test_image = temp_img(temp_file)

        if id == -1:
            return Club.objects.create(name=name, description=description, main_img=test_image.name, hours=commitment, is_visible=is_visible)
        else:
            return Club.objects.create(id=id, name=name, description=description, main_img=test_image.name, hours=commitment, is_visible=is_visible)

    return create_club


@pytest.fixture
def template_setup():
    temp_id = 9999

    SlideTemplates.templates = [
        SlideTemplates.Template(
            temp_id=temp_id, name="test", disabled=['body'])
    ]

    template = SlideTemplates.templates[0]
    return template


@pytest.fixture
def create_test_slide(db, temp_img, template_setup):
    def create_test_slide():
        template = template_setup
        # This creates a temporary image file to use for testing!!! The decorator overrides the django settings
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        test_image = temp_img(temp_file)

        # Parameters used for template
        slide_text = "this is a test"
        video_url = 'youtube.com/testing-video'
        args = [video_url, slide_text, test_image.name]
        template_args = ['video_url', 'text', 'img']

        return template, dict(zip(template_args, args))
    return create_test_slide


@pytest.fixture
def role_model_instances(create_club):
    def create():
        district1 = District.objects.create(name="d1")
        school1 = School.objects.create(name="s1")
        club1 = create_club()

        district1.add_school(school1)
        school1.add_club(club1)

        return (district1, school1, club1)
    return create


@pytest.fixture
def make_request():
    def make(client, method, *args, **kwargs):
        method_map = {
            'get': client.get,
            'post': client.post,
            'put': client.put,
            'patch': client.patch,
            'delete': client.delete,
            'head': client.head,
            'options': client.options,
            'trace': client.trace,
        }
        return method_map[method](*args, **kwargs)
    return make
