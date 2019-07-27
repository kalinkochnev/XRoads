from django.test import TestCase
from django.contrib.auth import get_user_model
from forum.models import SubForum, Post, Comment
from accounts.models import CustomUser


class ForumModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='test@user.com', alias='testuser', password='test_password')
        self.subforum = SubForum(name='Test Forum', description='testing description')
        self.post = None
        self.comment = Comment(user=self.user, text='test text', up_votes=10, down_votes=2)

    def test_SubForum_creation(self):
        self.assertEqual(self.subforum.name, 'Test Forum')
        self.assertEqual(self.subforum.description, 'testing description')

    def test_post_creation(self):
        self.post = Post(
            sub_forum=self.subforum,
            user=self.user,
            comment=self.comment,
            title='Test Title',
            text='Filler Test text',
            attached_file=None,
            up_votes=15,
            down_votes=1,
        )

        self.assertEqual(self.post.sub_forum, self.subforum)
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.comment, self.comment)
        self.assertEqual(self.post.title, 'Test Title')
        self.assertEqual(self.post.text, 'Filler Test text')
        self.assertEqual(self.post.attached_file, None)
        self.assertEqual(self.post.up_votes, 15)
        self.assertEqual(self.post.down_votes, 1)

    def test_comment_creation(self):
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.text, 'test text')
        self.assertEqual(self.comment.up_votes, 10)
        self.assertEqual(self.comment.down_votes, 2)
