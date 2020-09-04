from XroadsAPI.models import *
from XroadsAPI.serializers import *
from collections import OrderedDict
import tempfile
import pytest
from XroadsAPI.slide import SlideTemplates


def test_profile_serialization(db):
    user_obj: Profile = Profile.objects.create_user(
        email="a@email.com", password="password", first_name="a", last_name="b", is_anon=True)
    expected = {
        'id': user_obj.id,
        'email': user_obj.email,
        'first_name': user_obj.first_name,
        'last_name': user_obj.last_name,
        'is_anon': user_obj.is_anon,
    }

    assert expected == ProfileSerializer(user_obj).data


def test_profile_optional_fields(db):
    user_obj = Profile.objects.create_user(
        email="a@email.com", password="password", first_name="a", last_name="b")
    expected = {
        'id': user_obj.id,
        'email': user_obj.email,
        'first_name': user_obj.first_name,
        'last_name': user_obj.last_name,
        'is_anon': user_obj.is_anon,
    }

    assert expected == ProfileSerializer(user_obj).data


def test_profile_from_dict(db):
    user_obj: Profile = Profile(email="a@email.com", password="password",
                                first_name="a", last_name="b",is_anon=True)
    data = OrderedDict({
        'email': user_obj.email,
        'first_name': user_obj.first_name,
        'last_name': user_obj.last_name,
        'is_anon': user_obj.is_anon,
    })

    serializer = ProfileSerializer(data=data)
    serializer.is_valid()
    result: Profile = serializer.save()

    assert result.email == user_obj.email
    assert result.first_name == user_obj.first_name
    assert result.last_name == user_obj.last_name
    assert result.is_anon == user_obj.is_anon


@pytest.fixture
def gen_profiles(db, create_test_prof):
    def gen_profiles(num):
        visible = []
        invisible = []
        for i in range(num):
            if i % 2 == 0:
                visible.append(create_test_prof(num))
            else:
                invisible.append(create_test_prof(num))
        return visible, invisible


def test_anon_profile_remove_anon(db, gen_profiles, create_test_prof):
    prof1 = create_test_prof(1, is_anon=True)
    expected = {
        'is_anon': True
    }

    assert AnonProfileSerializer(prof1).data == expected


def test_anon_prof_not_anon_serialization(db, create_test_prof):
    prof1 = create_test_prof(1)
    expected = {
        'id': prof1.id,
        'email': prof1.email,
        'first_name': prof1.first_name,
        'last_name': prof1.last_name,
        'is_anon': prof1.is_anon,
    }

    assert AnonProfileSerializer(prof1).data == expected


def test_slide_serialization(db, temp_img, create_club):
    # Creates temp test iamge
    temp_file = tempfile.NamedTemporaryFile()
    test_image = temp_img(temp_file)

    video_url = "youtube.com/do-stuff"
    position = 1
    img = test_image.name

    # Set class variable to prevent conflicts
    temp_id = 1
    template_args = ['img', 'video_url']
    template = SlideTemplates.Template(
        temp_id=temp_id, name="test", required=template_args)
    SlideTemplates.templates = [template]
    club = create_club()

    # Chooses from test values based on template_args
    slide = SlideTemplates.new_slide(
        temp_id, club=club, position=position, img=img, video_url=video_url)

    expected = {
        'id': slide.id,
        'template_type': temp_id,
        'position': position,
        'video_url': video_url,
        'img': slide.img.url,
        'text': None,
        'club': club.id,
    }

    assert SlideSerializer(slide).data == expected


def test_club_creation(db, temp_img):
    # Creates temp test iamge
    temp_file = tempfile.NamedTemporaryFile()
    test_image = temp_img(temp_file)

    club: Club = Club.objects.create(
        name="a", description="b", main_img=test_image.name, hours="7hrs/week", is_visible=True)
    data = OrderedDict({
        'name': club.name,
        'description': club.description,
        'main_img': club.main_img.url,
        'hours': club.hours,
        'is_visible': club.is_visible,
        'members': [],
        'slides': [],
    })

    serializer = ClubDetailSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)
