from django.test import TestCase
from XroadsAPI.models import *
from XroadsAPI.serializers import *
from XroadsAPI.tests.test_models import get_temp_img, TestProfileModel
from django.test import override_settings
import pytest

import tempfile
class TestProfileSerializer(TestCase):
    def test_serialization(self):
        user_obj:Profile = Profile.objects.create_user(email="a@email.com", password="password", first_name="a", last_name="b", phone="1234567899", is_anon=True)
        expected = {
            'id': user_obj.id,
            'email': user_obj.email,
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name,
            'is_anon': user_obj.is_anon,
            'phone': user_obj.phone,
        }

        assert expected == ProfileSerializer(user_obj).data

    def test_optional_fields(self):
        user_obj = Profile.objects.create_user(email="a@email.com", password="password", first_name="a", last_name="b")
        expected = {
            'id': user_obj.id,
            'email': user_obj.email,
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name,
            'is_anon': user_obj.is_anon,
            'phone_num': None
        }

        assert expected == ProfileSerializer(user_obj).data

    def test_from_dict(self):
        user_obj:Profile = Profile(email="a@email.com", password="password", first_name="a", last_name="b", phone="1234567899", is_anon=True)
        data = {
            'email': user_obj.email,
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name,
            'is_anon': user_obj.is_anon,
            'phone': user_obj.phone,
        }

        serializer = ProfileSerializer(data=data)
        serializer.is_valid()
        result: Profile = serializer.save()

        assert result.email ==user_obj.email
        assert result.first_name == user_obj.first_name
        assert result.last_name == user_obj.last_name
        assert result.is_anon == user_obj.is_anon
        assert result.phone == user_obj.phone
        assert result.phone_num == user_obj.phone_num

class TestAnonProfileSerializer(TestCase):
    def generate_test_profiles(self, num):
        visible = []
        invisible = []
        for i in range(num):
            if i % 2 == 0:
                visible.append(TestProfileModel.create_test_prof(num))
            else:
                invisible.append(TestProfileModel.create_test_prof(num))
        return visible, invisible

    def test_remove_anon_profiles(self):
        prof1 = TestProfileModel.create_test_prof(1, is_anon=True)
        expected = {
            'is_anon': True
        }

        assert AnonProfileSerializer(prof1).data == expected
    
    def test_not_anon_serialization(self):
        prof1 = TestProfileModel.create_test_prof(1)
        expected = {
            'id': prof1.id,
            'email': prof1.email,
            'first_name': prof1.first_name,
            'last_name': prof1.last_name,
            'is_anon': prof1.is_anon,
            'phone_num': prof1.phone_num,
        }

        assert AnonProfileSerializer(prof1).data == expected
        
class TestMeetingDaySerializer(TestCase):
    def test_choices(self):
        day1 = MeetDay.objects.create(day=MeetDay.Day.MONDAY)
        assert MeetingDaysSerializer(day1).data == {'day': "MONDAY"}

        day2 = MeetDay.objects.create(day=MeetDay.Day.CUSTOM)
        assert MeetingDaysSerializer(day2).data == {'day': "CUSTOM"}

class TestSlideSerialization(TestCase):

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_slide_serialization(self):
        # Creates temp test iamge
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temp_img(temp_file)

        video_url= "youtube.com/do-stuff"
        position= 1
        img= test_image.name

        # Set class variable to prevent conflicts
        temp_id = 1
        template_args = ['img', 'video_url']
        template = SlideTemplates.Template(temp_id=temp_id, name="test", required=template_args)
        SlideTemplates.templates = [template]

        # Chooses from test values based on template_args
        slide = SlideTemplates.new_slide(temp_id, position=position, img=img, video_url=video_url)

        expected = {
            'id': slide.id,
            'template_type': temp_id,
            'position': position,
            'video_url': video_url,
            'img': slide.img.url,
            'text': None
        }


        assert SlideSerializer(slide).data == expected
