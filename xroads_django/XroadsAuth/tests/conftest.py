import pytest
from django.test import override_settings
from XroadsAPI.models import *
import tempfile
from PIL import Image


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

        temp_file = tempfile.NamedTemporaryFile()
        test_image = temp_img(temp_file)

        if id == -1:
            return Club.objects.create(name=name, description=description, main_img=test_image.name, hours=commitment, is_visible=is_visible)
        else:
            return Club.objects.create(id=id, name=name, description=description, main_img=test_image.name, hours=commitment, is_visible=is_visible)

    return create_club


@pytest.fixture
def create_test_prof(db):
    def create_test_prof2(num, **kwargs) -> Profile:
        from random import randint

        def gen_random_phone():
            chunk1 = randint(100, 999)
            chunk2 = randint(100, 999)
            chunk3 = randint(1000, 9999)
            return f'({chunk1}) {chunk2}-{chunk3}'
        params = {
            'email': f'test{num}@email.com',
            'password': 'password',
            'first': f'testfirst{num}',
            'last': f'testlast{num}',
            'phone': gen_random_phone(),
            'is_anon': False,
        }

        # overrides params if specified in kwargs
        for key, arg in kwargs.items():
            if key in params.keys():
                params[key] = arg

        return Profile.create_profile(email=params['email'], password=params['password'], first=params['first'], last=params['last'], phone=params['phone'], is_anon=params['is_anon'])
    return create_test_prof2


@pytest.fixture
def create_test_slide(db, temp_img):
    def create_test_slide():
        # Sets the class variable equal to this template to avoid conflicts with real code
        template_args = ['video_url', 'text', 'img']
        SlideTemplates.templates = [
            SlideTemplates.Template(
                temp_id=1, name="test", required=template_args)
        ]

        # This creates a temporary image file to use for testing!!! The decorator overrides the django settings
        temp_file = tempfile.NamedTemporaryFile()
        test_image = temp_img(temp_file)

        # Parameters used for template
        slide_text = "this is a test"
        video_url = 'youtube.com/testing-video'
        args = [video_url, slide_text, test_image.name]

        return SlideTemplates.templates[0], dict(zip(template_args, args))
    return create_test_slide
