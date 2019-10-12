import json

from django.http import JsonResponse
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.views.generic import ListView

from accounts.models import CustomUser
from forum.forms import TestAjaxForm
from forum.models import SubForum, Post, SchoolClass
from forum.views import ListPosts, FormRouter


class TestFormRouter(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.Router = FormRouter()
        self.Router.set_route_dict(dictionary={
            'action1': {
                'form': TestAjaxForm,
                'action_exceptions': ('Yay',)
            },

            'action2': {
                'form': TestAjaxForm,
                'action_exceptions': ()
            },

        })

    def test_request_valid(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data)
        self.Router.request = request
        self.assertTrue(self.Router.validate_request())

    def test_request_ajaxenforced_notajax(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data)
        self.Router.request = request
        self.Router.enforce_ajax = True
        self.assertFalse(self.Router.validate_request())

    def test_setup_dict_valid(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data)
        self.Router.request = request
        self.assertEqual(self.Router.setup_dict(), TestAjaxForm)

    def test_setup_dict_invalid(self):
        data = {
            'action': 'bad action',
        }
        request = self.factory.post('test/path', data=data)
        self.Router.request = request
        self.assertIsNone(self.Router.setup_dict())

    def test_update_args(self):
        self.Router.update_args(1, 2, 3, 4, **{'test': 123})
        self.assertEqual(self.Router.args, (1, 2, 3, 4))
        self.assertEqual(self.Router.kwargs, {'test': 123})

    def test_process_form(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data)
        self.Router.request = request
        self.Router.form = TestAjaxForm
        self.assertTrue(self.Router.process_form())

    def test_get_possible_exceptions(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data)
        self.Router.request = request
        self.assertEqual(self.Router.get_possible_exceptions(), ('Yay',))

    def test_form_do_action_exception(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data)
        self.Router.request = request
        self.Router.kwargs = {'throw_exception': True}
        with self.assertRaises(TypeError):
            self.Router.form_valid()

    def test_form_do_action_no_exception(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data)
        self.Router.request = request
        self.Router.kwargs = {'throw_exception': False}
        with self.assertRaises(TypeError):
            self.Router.form_valid()

    def test_route_request_valid(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data)
        self.Router.request = request
        self.assertEqual(self.Router.route(request=request), "Success!")

    def test_route_request_invalid(self):
        data = {
            'action': 'action32',
        }
        request = self.factory.post('test/path', data=data)
        self.Router.request = request
        self.assertEqual(self.Router.route(request=request), None)


class TestQuerySchoolClass(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('forumsapp:query/classes')

        self.teacher = CustomUser.objects.signup(email="teacher@email.com", alias="bestteacher", password="password")
        self.student1 = CustomUser.objects.signup(email="student@email.com", alias="student1", password="password")
        self.student2 = CustomUser.objects.signup(email="otherstudent@email.com", alias="student2", password="password")
        self.class1 = SchoolClass.objects.create(name="class 1", grade=11, placement="Honors", subject="art", teacher=self.teacher)
        self.class1.students.add(self.student1, self.student2)
        self.class2 = SchoolClass.objects.create(name="class 2", grade=11, placement="Honors", subject="art", teacher=self.teacher)
        self.class2.students.add(self.student1, self.student2)

    def test_GET(self):
        data = {
            'grade': 11,
            'subject': 'art',
        }
        response = self.client.get(self.url, data=data)

        print(response.content)
        correct_response = b"""[{"pk": 1, "fields": {"name": "class 1"}}, {"pk": 2, "fields": {"name": "class 2"}}]"""
        self.assertEqual(response.content, correct_response)

    def test_query_general(self):
        data = {
            'grade': 0,
            'subject': 'art',
        }
        response = self.client.get(self.url, data=data)

        print(response.content)
        correct_response = b"""[{"pk": 1, "fields": {"name": "class 1"}}, {"pk": 2, "fields": {"name": "class 2"}}]"""
        self.assertEqual(response.content, correct_response)


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('forumsapp:home')

    def test_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum_home.html')


# TODO make new tests for new layout
class TestListPosts(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@user.com', alias='testuser',
                                                   password='test_password')
        self.teacher = CustomUser.objects.signup(email="teacher@email.com", alias="bestteacher", password="password")
        self.student1 = CustomUser.objects.signup(email="student@email.com", alias="student1", password="password")
        self.class1 = SchoolClass.objects.create(name="class 1", grade=11, placement="Honors", teacher=self.teacher, subject="history")
        self.class1.students.add(self.student1)

        self.post = Post.objects.create(
            school_class=self.class1,
            user=self.user,
            title='Test Title',
            text='Filler Test body',
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
        self.user = CustomUser.objects.create_user(email='test@user.com', alias='testuser',
                                                   password='test_password')
        self.teacher = CustomUser.objects.signup(email="teacher@email.com", alias="bestteacher", password="password")
        self.student1 = CustomUser.objects.signup(email="student@email.com", alias="student1", password="password")
        self.class1 = SchoolClass.objects.create(name="class 1", grade=11, placement="Honors", teacher=self.teacher, subject="language")
        self.class1.students.add(self.student1)
        self.post = Post.objects.create(
            school_class=self.class1,
            user=self.user,
            title='Test Title',
            text='Filler Test body',
        )
        self.client = Client()
        self.post_detail_url = reverse('forumsapp:forum_post',
                                       kwargs={'forum_name': self.class1.url_name, 'post_id': self.post.id, })
        self.factory = RequestFactory()

    def test_GET(self):
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post.html')


class TestCreatePostView(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.signup(email="teacher@email.com", alias="bestteacher",
                                                 password="password")
        self.school_class = SchoolClass.objects.create(name="class 1", grade=11, placement="AP", teacher=self.teacher, subject="math")
        self.user = CustomUser.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')
        self.client = Client()
        self.create_post_url = reverse('forumsapp:post/create')

    def test_GET(self):
        response = self.client.get(self.create_post_url)
        self.assertEqual(response.status_code, 405)

    def test_POST_create_post(self):
        data = {
            'title': 'Test Post',
            'text': 'Testing body',
            'grade_input': 11,
            'subject_input': 'math',
            'schoolclass_field': self.school_class.id,
        }

        self.client.login(email="norm@user.com", password="testpassword")
        response = self.client.post(self.create_post_url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)

    def test_POST_create_post_bad(self):
        data = {
            'title': 'Test Post',
            'text': 'Testing body',
            'schoolclass_field': '',
        }

        self.client.login(email="norm@user.com", password="testpassword")
        response = self.client.post(self.create_post_url, data=data, follow=True,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)


class TestTOSView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')
        self.client = Client()
        self.tos_url = reverse('forumsapp:tos')

    def test_GET(self):
        response = self.client.get(self.tos_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/tos.html')


class TestPrivacyView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')
        self.client = Client()
        self.pp_url = reverse('forumsapp:pp')

    def test_GET(self):
        response = self.client.get(self.pp_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/pp.html')