from django.http import JsonResponse
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.views.generic import ListView

from accounts.models import CustomUser
from forum.forms import TestAjaxForm
from forum.models import SubForum, Post
from forum.views import MultiAjaxHandler, ListPosts


class TestMultiAjaxHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.majax = MultiAjaxHandler()
        self.majax.handler_dict = {
            'action1': 'form1',
            'action2': 'form2',
        }

    def test_request_is_valid_noajax(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data)
        self.majax.request = request
        self.assertFalse(self.majax.request_is_valid())

    def test_request_is_valid_wrong_action(self):
        data = {
            'action': 'doesnotexist',
        }
        request = self.factory.post('test/path', data=data)
        self.majax.request = request
        self.assertFalse(self.majax.request_is_valid())

    def test_request_is_valid_no_data(self):
        data = {}
        request = self.factory.post('test/path', data=data)
        self.majax.request = request
        self.assertFalse(self.majax.request_is_valid())

    def test_request_is_valid_withajax(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.majax.request = request
        self.assertTrue(self.majax.request_is_valid())

    def test_request_is_valid_withajax_wrongdata(self):
        data = {
            'action': 'wrongaction',
        }
        request = self.factory.post('test/path', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.majax.request = request
        self.assertFalse(self.majax.request_is_valid())

    # Test that the correct dict value is returned
    def test_ajax_router(self):
        data = {
            'action': 'action2',
        }
        request = self.factory.post('test/path', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.majax.request = request
        self.assertEqual(self.majax.action_router(), 'form2')


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('forumsapp:home')

    def test_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/home.html')


class TestListPosts(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@user.com', alias='testuser', password='test_password')
        self.subforum = SubForum.objects.create(name='Test Forum', description='testing description')
        self.post = Post.objects.create(
            sub_forum=self.subforum,
            user=self.user,
            title='Test Title',
            text='Filler Test text',
            attached_file=None,
        )
        self.client = Client()
        self.forum_url = reverse('forumsapp:forum', kwargs={'forum_name': self.subforum.url_name})
        self.factory = RequestFactory()

    def test_GET(self):
        response = self.client.get(self.forum_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum.html')

    def test_POST_upvote(self):
        data = {
            'action': 'upvote',
            'post_id': self.post.id,
        }

        self.client.login(email="test@user.com", password="test_password")
        request = self.client.post(self.forum_url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.post.upvote_count, 1)
        self.assertEqual(self.post.downvote_count, 0)

    def test_POST_downvote(self):
        data = {
            'action': 'downvote',
            'post_id': self.post.id,
        }

        self.client.login(email="test@user.com", password="test_password")
        request = self.client.post(self.forum_url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.post.upvote_count, 0)
        self.assertEqual(self.post.downvote_count, 1)

    def test_POST_clearvote(self):
        data = {
            'action': 'downvote',
            'post_id': self.post.id,
        }

        self.client.login(email="test@user.com", password="test_password")
        request = self.client.post(self.forum_url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.post.upvote_count, 0)
        self.assertEqual(self.post.downvote_count, 1)

        data = {
            'action': 'clearvote',
            'post_id': self.post.id,
        }

        request = self.client.post(self.forum_url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.post.upvote_count, 0)
        self.assertEqual(self.post.downvote_count, 0)


class TestPostDetail(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@user.com', alias='testuser', password='test_password')
        self.subforum = SubForum.objects.create(name='Test Forum', description='testing description')
        self.post = Post.objects.create(
            sub_forum=self.subforum,
            user=self.user,
            title='Test Title',
            text='Filler Test text',
            attached_file=None,
        )
        self.client = Client()
        self.post_detail_url = reverse('forumsapp:forum_post',
                                       kwargs={'forum_name': self.subforum.url_name, 'post_id': self.post.id, })
        self.factory = RequestFactory()

    def test_GET(self):
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post.html')


class TestCreatePostView(TestCase):
    def setUp(self):
        self.subforum = SubForum.objects.create(name='Test Forum', description='testing description')
        self.user = CustomUser.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')
        self.client = Client()
        self.create_post_url = reverse('forumsapp:create_post')

    def test_GET(self):
        response = self.client.get(self.create_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/create_post.html')

    def test_POST_create_post(self):
        data = {
            'title': 'Test Post',
            'text': 'Testing text',
            'attached_file': "",
            'subforum': str(self.subforum),
        }

        self.client.login(email="norm@user.com", password="testpassword")
        response = self.client.post(self.create_post_url, data=data, follow=True)
        self.assertRedirects(response, reverse('forumsapp:home'), 302, 200)


class TestTOSView(TestCase):
    def setUp(self):
        self.subforum = SubForum.objects.create(name='Test Forum', description='testing description')
        self.user = CustomUser.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')
        self.client = Client()
        self.tos_url = reverse('forumsapp:tos')

    def test_GET(self):
        response = self.client.get(self.tos_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/tos.html')


class TestPrivacyView(TestCase):
    def setUp(self):
        self.subforum = SubForum.objects.create(name='Test Forum', description='testing description')
        self.user = CustomUser.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')
        self.client = Client()
        self.pp_url = reverse('forumsapp:pp')

    def test_GET(self):
        response = self.client.get(self.pp_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/pp.html')
