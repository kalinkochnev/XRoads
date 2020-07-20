from django.contrib.auth.models import User
from django.core.exceptions import FieldError

from django.test import TestCase
from django.test import override_settings
from parameterized import parameterized

from XroadsAPI.models import Profile, SlideTemplates, Club, MeetDay, Faq
from XroadsAPI.exceptions import *

# Tests needing a temporary image file
import tempfile
from PIL import Image


def get_temp_img(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGB", size, color)
    image.save(temp_file, 'jpeg')
    return temp_file


class TestProfileModel(TestCase):
    def setUp(self):
        self.email = "kalin.kochnev@gmail.com"
        self.password = "2323hj23hk2h"
        self.first_name = "kalin"
        self.last_name = "kochnev"
        self.phone_number_str = '518-888-1542'
        self.phone_number_int = 5188881542
        self.is_anon = True

    @parameterized.expand([
        # phone number, expected value
        ['518-888-1542', "5188881542"],
        ['(518) 888-1542', "5188881542"],
        ['518 888 1542', "5188881542"],
        ['5 1 8 8 8 8 1 5 4 2', "5188881542"]
    ])
    def test_parse_phone_valid_len(self, input_phone, expected):
        self.assertEqual(Profile.parse_phone(input_phone), expected)

    @parameterized.expand(['518-888-154211111', '123-4567', '12345678'])
    def test_parse_phone_invalid_len(self, input_phone):
        with self.assertRaises(FieldError) as context:
            Profile.parse_phone(input_phone)

    def test_creation_optional(self):
        prof: Profile = Profile.create_profile(email=self.email, password=self.password, first=self.first_name,
                                               last=self.last_name)
        self.assertIsNone(prof.phone_num)
        self.assertFalse(prof.is_anon)

        user_obj = prof.user
        self.assertEqual(user_obj.first_name, self.first_name)
        self.assertEqual(user_obj.last_name, self.last_name)
        self.assertEqual(user_obj.email, self.email)

    def test_creation_all_params(self):
        prof: Profile = Profile.create_profile(email=self.email, password=self.password, first=self.first_name,
                                               last=self.last_name, phone=self.phone_number_str, is_anon=self.is_anon)
        self.assertEqual(prof.phone_num, self.phone_number_int)
        self.assertEqual(prof.is_anon, self.is_anon)


class TestTemplate(TestCase):
    def setUp(self):
        self.temp_id = 9999
        self.template_args = ['video_url', 'text', 'img']

        SlideTemplates.templates = [
            SlideTemplates.Template(
                temp_id=self.temp_id, name="test", required=self.template_args)
        ]

        self.template = SlideTemplates.templates[0]

    def test_match_args_valid(self):
        test_args = ['text', 'video_url', 'img', 'position']
        self.assertTrue(self.template.args_match(test_args))

    def test_position_arg_required(self):
        test_args = ['text', 'video_url', 'img']
        self.assertFalse(self.template.args_match(test_args))

    def test_match_args_invalid(self):
        test_args = ['text']
        self.assertFalse(self.template.args_match(test_args))

    def test_get_template(self):
        self.assertEqual(SlideTemplates.get(self.temp_id), self.template)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_slide(self):
        # This creates a temporary image file to use for testing!!! The decorator overrides the django settings
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temp_img(temp_file)

        slide_text = "this is a test"
        video_url = 'youtube.com/testing-video'
        args = [video_url, slide_text, test_image.name]

        template_kwargs = dict(zip(self.template_args, args))
        slide = SlideTemplates.new_slide(
            self.temp_id, position=1, **template_kwargs)

        self.assertIsNotNone(slide.img)
        self.assertEqual(slide.img, test_image)
        self.assertEqual(slide.text, slide_text)
        self.assertEqual(slide.video_url, video_url)

    def test_create_invalid_slide(self):
        with self.assertRaises(SlideParamError) as e:
            SlideTemplates.new_slide(self.temp_id, position=1)

    @classmethod
    def create_test_slide(cls):
        # Sets the class variable equal to this template to avoid conflicts with real code
        template_args = ['video_url', 'text', 'img']
        SlideTemplates.templates = [
            SlideTemplates.Template(temp_id=1, name="test", required=template_args)
        ]
        
        # This creates a temporary image file to use for testing!!! The decorator overrides the django settings        
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temp_img(temp_file)

        # Parameters used for template
        slide_text = "this is a test"
        video_url = 'youtube.com/testing-video'
        args = [video_url, slide_text, test_image.name]

        return SlideTemplates.templates[0], dict(zip(template_args, args))


class TestCreateClub(TestCase):
    def setUp(self):
        self.profile = Profile.create_profile(
            email="a@gmail.com", password="password", first="kalin", last="kochnev", phone="518-888-1548")
        self.name = "Test Club"
        self.description = "This is a club description"
        self.commitment = "7hrs/week"
        self.is_visible = False

        temp_file = tempfile.NamedTemporaryFile()
        self.test_image = get_temp_img(temp_file)

        self.club: Club = Club.objects.create(name=self.name, description=self.description,
                                              main_img=self.test_image.name, hours=self.commitment, is_visible=self.is_visible)

    def test_add_meet_day(self):
        day_obj1 = self.club.add_meet_day(MeetDay.Day.MONDAY)
        day_obj2 = self.club.add_meet_day(MeetDay.Day.TUESDAY)

        self.assertEqual(self.club.meeting_days.count(), 2)
        self.assertEqual(self.club.meeting_days.get(
            day=MeetDay.Day.MONDAY), day_obj1)
        self.assertEqual(self.club.meeting_days.get(
            day=MeetDay.Day.TUESDAY), day_obj2)

        # Test that if you add same day it doesn't duplicate
        day_obj = self.club.add_meet_day(MeetDay.Day.MONDAY)
        self.assertEqual(self.club.meeting_days.count(), 2)

    def test_remove_meet_day(self):
        day_obj = self.club.add_meet_day(MeetDay.Day.MONDAY)

        self.club.remove_meet_day(MeetDay.Day.MONDAY)
        self.assertEqual(self.club.meeting_days.count(), 0)

    def test_add_faq_question(self):
        faq1 = self.club.add_faq_question("my question", "my answer")
        faq2 = self.club.add_faq_question("my question", "my answer")

        self.assertEqual(self.club.faq.count(), 2)
        self.assertEqual(faq1.position, 1)
        self.assertEqual(faq2.position, 2)

    def test_remove_faq_question(self):
        faq1 = self.club.add_faq_question("my question", "my answer")
        faq2 = self.club.add_faq_question("my question", "my answer")

        self.club.remove_faq_question(1)

        self.assertEqual(self.club.faq.count(), 1)

    def test_add_slide(self):
        template, params = TestTemplate.create_test_slide()
        slide1 = self.club.add_slide(template.temp_id, **params)
        slide2 = self.club.add_slide(template.temp_id, **params)

        self.assertEqual(self.club.slides.count(), 2)
        self.assertEqual(slide1.position, 1)
        self.assertEqual(slide2.position, 2)

    def test_remove_slide(self):
        template, params = TestTemplate.create_test_slide()
        slide1 = self.club.add_slide(template.temp_id, **params)
        
        self.club.remove_slide(1)
        self.assertEqual(self.club.slides.count(), 0)