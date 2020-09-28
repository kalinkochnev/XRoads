import pytest
from django.test import override_settings
from XroadsAPI.models import *
from XroadsAuth.models import Profile
import tempfile
from PIL import Image
from XroadsAPI.slide import SlideTemplates
from rest_framework.test import APIClient
from XroadsAuth.permissions import Role


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
def create_test_prof(db):
    
    def create_test_prof2(num, **kwargs) -> Profile:
        params = {
            'email': f'test{num}@email.com',
            'password': 'password',
            'first': f'testfirst{num}',
            'last': f'testlast{num}',
            'is_anon': False,
        }

        # overrides params if specified in kwargs
        for key, arg in kwargs.items():
            if key in params.keys():
                params[key] = arg

        return Profile.create_profile(email=params['email'], password=params['password'], first=params['first'], last=params['last'], is_anon=params['is_anon'])
    return create_test_prof2


@pytest.fixture
def template_setup():
    temp_id = 9999
    template_args = ['video_url', 'text', 'img']

    SlideTemplates.templates = [
        SlideTemplates.Template(
            temp_id=temp_id, name="test", required=template_args)
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
        template_args = template.required_args

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
def perm_const_override():
    import XroadsAuth.permisson_constants as PermConst

    PermConst.DISTRICT_ADMIN = 'District Admin'
    PermConst.SCHOOL_ADMIN = 'School Admin'
    PermConst.CLUB_EDITOR = 'Club Editor'
    PermConst.ROLE_HIERARCHY = PermConst.Hierarchy(District, School, Club, name=PermConst.CLUB_EDITOR)

    # Roles go from highest level to lowest level in ROLES list 
    PermConst.ROLES = [
        PermConst.Hierarchy(District, name=PermConst.DISTRICT_ADMIN, poss_perms=['__all__', 'create-school', 'modify-district']),
        PermConst.Hierarchy(District, School, name=PermConst.SCHOOL_ADMIN, poss_perms=['__all__', 'create-club', 'modify-school', 'hide-club', 'view-user-detail', 'hide-school']),
        PermConst.Hierarchy(District, School, Club, name=PermConst.CLUB_EDITOR, poss_perms=['__all__', 'modify-club', 'add-admin', 'hide-club', 'answer-questions']),
    ]




@pytest.fixture
def actual_perm_const():
    import XroadsAuth.permisson_constants as PermConst
    from importlib import reload  
    reload(PermConst)

@pytest.fixture
def setup_client_no_auth():
    def setup():
        client = APIClient()
        return client
    return setup


@pytest.fixture
def setup_client_auth(create_test_prof, setup_client_no_auth):
    def setup(prof_num=1):
        profile = create_test_prof(prof_num)
        client = setup_client_no_auth()
        client.force_authenticate(user=profile)
        return profile, client
    return setup

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


@pytest.fixture
def prof_w_perm(setup_client_auth):
    def setup(model, prof_num=1, perms=[]):
        prof, client = setup_client_auth(prof_num)
        role = Role.from_start_model(model)
        role.permissions.add(*perms)
        role.give_role(prof)
        return prof, client
    return setup