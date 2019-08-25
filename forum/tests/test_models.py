from django.test import TestCase
from django.contrib.auth import get_user_model
from forum.models import SubForum, Post, Comment
from accounts.models import CustomUser


class ForumModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='test@user.com', alias='testuser', password='test_password')
        self.subforum = SubForum.objects.create(name='Test Forum', description='testing description')
        self.post = Post.objects.create(
            sub_forum=self.subforum,
            user=self.user,
            title='Test Title',
            text='Filler Test text',
            attached_file=None,
        )

        self.comment = Comment.objects.create(user=self.user, post=self.post, text='test text')

    def test_SubForum_creation(self):
        self.assertEqual(self.subforum.name, 'Test Forum')
        self.assertEqual(self.subforum.description, 'testing description')

    def test_post_creation(self):

        self.assertEqual(self.post.sub_forum, self.subforum)
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.title, 'Test Title')
        self.assertEqual(self.post.text, 'Filler Test text')
        self.assertEqual(self.post.attached_file, None)

    def test_comment_filtering_by_post(self):
        self.assertEqual(Comment.objects.get(post=self.post.id), self.comment)

    def test_post_add_votes(self):
        self.post.upvotes.add(self.user)
        self.assertEqual(self.post.upvote_count, 1)
        self.post.downvotes.add(self.user)
        self.assertEqual(self.post.downvote_count, 1)

    def test_post_remove_votes(self):
        self.post.upvotes.remove(self.user)
        self.assertEqual(self.post.upvote_count, 0)
        self.post.downvotes.remove(self.user)
        self.assertEqual(self.post.downvote_count, 0)

    def test_comment_creation(self):
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.text, 'test text')
        # TODO add voting to comment

    def test_upvote_no_prev_vote(self):
        self.post.upvote(self.user)
        self.assertEqual(self.post.upvote_count, 1)
        self.assertEqual(self.post.downvote_count, 0)

    def test_upvote_with_prev_upvote(self):
        self.post.upvote(self.user)
        self.assertEqual(self.post.upvote_count, 1)
        self.post.upvote(self.user)
        self.assertEqual(self.post.upvote_count, 1)

    def test_upvote_with_prev_downvote(self):
        self.post.downvote(self.user)
        self.assertEqual(self.post.downvote_count, 1)
        self.post.upvote(self.user)
        self.assertEqual(self.post.upvote_count, 1)
        self.assertEqual(self.post.downvote_count, 0
                         )

    def test_downvote_no_prev_vote(self):
        self.post.downvote(self.user)
        self.assertEqual(self.post.upvote_count, 0)
        self.assertEqual(self.post.downvote_count, 1)

    def test_downvote_with_prev_upvote(self):
        self.post.downvote(self.user)
        self.assertEqual(self.post.downvote_count, 1)
        self.post.downvote(self.user)
        self.assertEqual(self.post.downvote_count, 1)

    def test_downvote_with_prev_downvote(self):
        self.post.upvote(self.user)
        self.assertEqual(self.post.upvote_count, 1)
        self.post.downvote(self.user)
        self.assertEqual(self.post.downvote_count, 1)
        self.assertEqual(self.post.upvote_count, 0)

    def test_clearvote(self):
        self.post.clearvote(self.user)
        self.assertEqual(self.post.upvote_count, 0)
        self.assertEqual(self.post.downvote_count, 0)
