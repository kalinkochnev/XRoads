from django.test import TestCase
from accounts.models import CustomUser
from accounts.forms import SignupForm, LoginForm


class TestSignupForm(TestCase):
    # TODO add form field cleaning tests

    # testing with all correct fields
    def test_valid_fields(self):
        form_data = {
            'email': 'valid@gmail.com',
            'alias': 'validalias',
            'password': 'validpassword',
            'confirm_pass': 'validpassword'
        }
        form = SignupForm(form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_fields(self):
        form_data = {
            'email': 'validgmail.com',
            'alias': 'validalias',
            'password': 'notvalidpassword',
            'confirm_pass': 'validpassword'
        }
        form = SignupForm(form_data)
        self.assertFalse(form.is_valid())

    def test_password_matching(self):
        form_data = {
            'email': 'validgmail.com',
            'alias': 'validalias',
            'password': 'wrongpass',
            'confirm_pass': 'validpassword'
        }
        form = SignupForm(form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'email': 'validgmail.com',
            'alias': 'validalias',
            'password': 'wrongpass',
            'confirm_pass': 'validpassword'
        }
        form = SignupForm(form_data)
        self.assertFalse(form.is_valid())

    def test_data_is_blank(self):
        form_data = {}
        form = SignupForm(form_data)
        self.assertFalse(form.is_valid())


class TestLoginForm(TestCase):
    def setUp(self):
        new_user = CustomUser.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')

    def test_valid_fields(self):
        def test_valid_fields(self):
            form_data = {
                'email': 'valid@gmail.com',
                'password': 'validpassword',
            }
            form = LoginForm(form_data)
            self.assertIsNotNone(form.is_valid())

    def test_data_is_blank(self):
        form_data = {}
        form = LoginForm(form_data)
        self.assertFalse(form.is_valid())
