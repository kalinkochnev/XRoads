from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from urllib.parse import urlencode


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

    # Test GET, POST request, No data
    def test_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_POST_no_data(self):
        response = self.client.post(self.login_url, {}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_POST_correct_data(self):
        new_user = CustomUser.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')
        login_form_data = {
            'email': 'norm@user.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, login_form_data, follow=True)
        self.assertRedirects(response, reverse('forumsapp:home'), 302, 200)

    def test_POST_incorrect_data(self):
        signup_data = {
            'email': 'norm@user.com',
            'alias': 'testuser',
            'password': 'wrongpass',
            'confirm_pass': 'testpassword'
        }
        response = self.client.post(self.login_url, data=signup_data, follow=True)
        self.assertEqual(response.status_code, 200)


class TestSignupView(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    # Test GET, POST request, No data
    def test_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_POST_no_data(self):
        response = self.client.post(self.signup_url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_POST_correct_data(self):
        signup_data = {
            'email': 'norm@user.com',
            'alias': 'testuser',
            'password': 'testpassword',
            'confirm_pass': 'testpassword'
        }
        response = self.client.post(self.signup_url, data=signup_data, follow=True)
        self.assertRedirects(response, reverse('forumsapp:home'), 302, 200)

    def test_POST_incorrect_data(self):
        signup_data = {
            'email': 'norm@user.com',
            'alias': 'testuser',
            'password': 'wrongpass',
            'confirm_pass': 'testpassword'
        }
        response = self.client.post(self.signup_url, data=signup_data, follow=True)
        self.assertEqual(response.status_code, 200)
