from django import forms
from django.test import TestCase
from accounts.models import CustomUser
from forum.forms import TestAjaxForm, VotePostForm, CreatePostForm
from forum.models import Post, SubForum, SchoolClass
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
        self.school_class = SchoolClass.objects.create(name="test_class", grade=11, placement="Honors", teacher=self.user)
        self.post = Post.objects.create(
            school_class=self.school_class,
            user=self.user,
            title='Test Title',
            text='Filler Test body',
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
        # TODO make signup for teachers
        self.teacher = CustomUser.objects.signup(email="teacher@email.com", alias="bestteacher", password="password")
        self.school_class = SchoolClass.objects.create(name="class 1", grade=11, placement="AP",  teacher=self.teacher, subject="science")
        self.user = CustomUser.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')

    def test_valid_fields(self):
        data = {
            'title': 'Test Title',
            'text': 'Test post text',
            'schoolclass_field': self.school_class.id,
            'grade': 11,
            'subject_input': 'history',
        }
        Form = CreatePostForm(data)
        self.assertTrue(Form.is_valid())

    # TODO validate the file field
    @skip("The File field has no validator created yet")
    def test_invalid_file(self):
        data = {
            'action': 'create-post',
            'title': 'Test Title',
            'text': 'Test post text',
            'school_class_id': self.school_class.id,
        }
        Form = CreatePostForm(data)
        self.assertFalse(Form.is_valid())
