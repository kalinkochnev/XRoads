from django import forms
from django.test import TestCase
from accounts.models import CustomUser
from forum.forms import TestAjaxForm, VotePostForm, CreatePostForm
from forum.models import Post, SubForum
from unittest import skip


class TestAjaxTestForm(TestCase):

    def test_correct_data(self):
        data = {
            'action': 'someaction',
        }
        form = TestAjaxForm(data)
        self.assertTrue(form.is_valid())

    def test_blank(self):
        data = {}
        form = TestAjaxForm(data)
        self.assertFalse(form.is_valid())


class TestVotingForm(TestCase):

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

    def test_action_valid_clean(self):
        data = {
            'action': 'upvote',
            'post_id': self.post.id,
        }
        Form = VotePostForm(data)

        self.assertTrue(Form.is_valid())

    def test_action_invalid_clean(self):
        data = {'action': 'bad data'}
        Form = VotePostForm(data)

        self.assertFalse(Form.is_valid())

    def test_post_id_valid_clean(self):
        data = {
            'action': 'upvote',
            'post_id': self.post.id,
        }
        Form = VotePostForm(data)

        self.assertTrue(Form.is_valid())

    def test_post_id_invalid_clean(self):
        data = {
            'action': 'upvote',
            'post_id': self.post.id + 1,
        }
        Form = VotePostForm(data)

        self.assertFalse(Form.is_valid())


# TODO add tests for file field
class TestCreatePostForm(TestCase):

    def setUp(self):
        self.subforum = SubForum.objects.create(name='Test Forum', description='testing description')
        self.user = CustomUser.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')

    def test_valid_fields(self):
        data = {
            'title': 'Test Post',
            'text': 'Testing text',
            'attached_file': None,
            'subforum': str(self.subforum),
        }
        Form = CreatePostForm(data)
        self.assertTrue(Form.is_valid())

    # TODO validate the file field
    @skip("The File field has no validator created yet")
    def test_invalid_file(self):
        data = {
            'title': 'Test Post',
            'text': 'Testing text',
            'attached_file': " ",
            'subforum': str(self.subforum),
        }
        Form = CreatePostForm(data)
        self.assertFalse(Form.is_valid())

    def test_create_post(self):
        data = {
            'title': 'Test Title',
            'text': 'Filler Test text',
            'attached_file': None,
            'subforum': str(self.subforum),
        }
        Form = CreatePostForm(data)
        self.assertTrue(Form.is_valid())
        Form.create_post(user_obj=self.user)

        self.assertTrue(Post.objects.filter(title='Test Title').exists())
        post = Post.objects.get(title='Test Title')
        self.assertEqual(post.title, 'Test Title')
        self.assertEqual(post.text, 'Filler Test text')
        self.assertEqual(post.sub_forum, self.subforum)
