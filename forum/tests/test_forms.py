from django import forms
from django.test import TestCase
from accounts.models import CustomUser
from forum.forms import TestAjaxForm, VotePostForm
from forum.models import Post, SubForum


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
