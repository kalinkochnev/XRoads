from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import override_settings
from parameterized import parameterized
from django.contrib.auth import get_user_model, authenticate

from XroadsAPI.models import *
from XroadsAPI.exceptions import *

# Tests needing a temporary image file
import tempfile
from PIL import Image

# TODO test that that the objects are saved after calling their methods
class TestCustomUserModel(TestCase):
    # gets run before every method call of the test
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='norm@user.com', password='testpassword')

    def test_norm_user_creation(self):
        self.assertEqual(self.user.email, 'norm@user.com')
        # TODO Test when the user has the same username and tag that the tag becomes different

        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

        # test username attribute does not exist because it shouldn't
        try:
            self.assertIsNone(self.user.username)
        except AttributeError:
            pass

        # test when certain parameters are missing it raises the errors
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(TypeError):
            self.User.objects.create_user(username='testuser', password='testpassword')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='norm@user.com', username='testuser', password='')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', username='', password='')

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        # test username attribute does not exist
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass

        # tests that if is_superuser=False that it raises an error
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False
            )

    def test_authentication(self):
        # check that auth returns a user object that is the expected one
        user_email = 'email@user.com'
        user_password = 'testpassword'
        user1 = self.User.objects.create_user(email=user_email, password=user_password)
        returned_user = authenticate(email=user_email, password=user_password)
        self.assertEqual(user1, returned_user)

        # check that None is returned if password is incorrect
        user_email = 'email@user.com'
        user_wrong_password = 'yikes'
        user2 = self.User.objects.create_user(email='email2@user.com', password='testpassword')
        returned_user = authenticate(email=user_email, password=user_wrong_password)
        self.assertIsNone(returned_user)

    def test_signup(self):
        # should return a user object since it doesn't exist
        user_email = 'new@email.com'
        user_pass = 'somepass'
        new_user = self.User.objects.signup(user_email, user_pass)
        self.assertEqual(new_user.email, user_email)
        self.assertTrue(new_user.check_password(user_pass))

        # should return none since user with that email already exists
        other_user = self.User.objects.signup(user_email, 'password')
        self.assertIsNone(other_user)


def get_temp_img(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGB", size, color)
    image.save(temp_file, 'jpeg')
    return temp_file


class TestProfileModel(TestCase):
    @classmethod
    def create_test_prof(cls, num, **kwargs) -> Profile:
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

        self.assertEqual(prof.first_name, self.first_name)
        self.assertEqual(prof.last_name, self.last_name)
        self.assertEqual(prof.email, self.email)

        # test second object is created normally (Added due to bug where you can't only use email and password for User model creation)
        prof2 = Profile.create_profile(email="something@gmail.com", password="a", first="b", last="c")


    def test_creation_all_params(self):
        prof: Profile = Profile.create_profile(email=self.email, password=self.password, first=self.first_name,
                                               last=self.last_name, phone=self.phone_number_str, is_anon=self.is_anon)
        self.assertEqual(prof.phone_num, self.phone_number_int)
        self.assertEqual(prof.is_anon, self.is_anon)

    def test_create_test_prof(self):
        # Test that valid attributes are set
        prof_num = 1
        prof = self.create_test_prof(prof_num)
        self.assertEqual(prof.email, f'test{prof_num}@email.com')
        self.assertEqual(len(prof.phone), 10)
        self.assertEqual(prof.first_name, f'testfirst{prof_num}')
        self.assertEqual(prof.last_name, f'testlast{prof_num}')

        # Test that you can override params
        prof_num = 2
        test_email = 'hello@gmail.com'
        prof2 = self.create_test_prof(prof_num, email=test_email)
        self.assertEqual(prof2.email, test_email)

    def test_join_school(self):
        school = School.objects.create(name="Some School")
        prof: Profile = Profile.create_profile(email=self.email, password=self.password, first=self.first_name,
                                               last=self.last_name, phone=self.phone_number_str, is_anon=self.is_anon)
        prof.join_school(school)
        self.assertEqual(school.students.count(), 1)

    def test_school_property(self):
        school = School.objects.create(name="Some School")
        prof: Profile = Profile.create_profile(email=self.email, password=self.password, first=self.first_name,
                                               last=self.last_name, phone=self.phone_number_str, is_anon=self.is_anon)
        prof.join_school(school)
        self.assertEqual(school, prof.school)


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
            SlideTemplates.Template(
                temp_id=1, name="test", required=template_args)
        ]

        # This creates a temporary image file to use for testing!!! The decorator overrides the django settings
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temp_img(temp_file)

        # Parameters used for template
        slide_text = "this is a test"
        video_url = 'youtube.com/testing-video'
        args = [video_url, slide_text, test_image.name]

        return SlideTemplates.templates[0], dict(zip(template_args, args))


class TestClub(TestCase):
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

    @classmethod
    def create_test_club(cls):
        name = "Test Club"
        description = "This is a club description"
        commitment = "7hrs/week"
        is_visible = False

        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temp_img(temp_file)

        return Club.objects.create(name=name, description=description, main_img=test_image.name, hours=commitment, is_visible=is_visible)

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

    def test_join(self):
        self.club.join(self.profile)
        self.assertEqual(self.club.members.count(), 1)

    def test_leave(self):
        self.club.join(self.profile)
        self.club.leave(self.profile)

        self.assertEqual(self.club.members.count(), 0)


class TestSchool(TestCase):
    def test_add_club(self):
        club = TestClub.create_test_club()
        school = School.objects.create(name="Some School")
        school.add_club(club)

        self.assertEqual(school.clubs.count(), 1)
