from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from forum.models import SubForum, Post, Comment, SchoolClass
from accounts.models import CustomUser


class SchoolClassTests(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.signup(email="teacher@email.com", alias="bestteacher", password="password")
        self.student1 = CustomUser.objects.signup(email="student@email.com", alias="student1", password="password")
        self.student2 = CustomUser.objects.signup(email="otherstudent@email.com", alias="student2", password="password")
        self.SchoolClass = SchoolClass.objects.create(name='class 1', grade=11, placement="Honors",teacher=self.teacher, subject="math")
        self.SchoolClass.students.add(self.student1, self.student2)

    def test_SchoolClass_creation(self):
        self.assertEqual(self.SchoolClass.name, 'class 1')
        self.assertEqual(self.SchoolClass.grade, 11)
        self.assertEqual(self.SchoolClass.placement, "Honors")
        self.assertEqual(str(self.SchoolClass), "class 1 11 Honors")

    def test_SchoolClass_teacher(self):
        self.assertEqual(SchoolClass.objects.get(teacher=self.teacher), self.SchoolClass)

    def test_SchoolClass_students(self):
        self.assertEqual(self.SchoolClass.students.count(), 2)


class ForumModelTests(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(email='test@user.com', alias='testuser', password='test_password')
        self.post_class = SchoolClass.objects.create(
            name="Test Class",
            grade=11,
            placement="Honors",
            teacher=self.user,
            subject="music",
        )
        self.post = Post.objects.create(
            school_class=self.post_class,
            user=self.user,
            title='Test Title',
            text='Filler Test body',
        )

        self.comment = Comment.objects.create(user=self.user, post=self.post, text='test body')

    def test_SchoolClass_creation(self):
        self.assertEqual(self.post_class.name, 'Test Class')
        self.assertEqual(self.post_class.grade, 11)
        self.assertEqual(self.post_class.placement, "Honors")
        self.assertEqual(self.post_class.teacher, self.user)
        self.assertEqual(self.post_class.subject, "music")

    def test_post_creation(self):
        self.assertEqual(self.post.school_class, self.post_class)
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.title, 'Test Title')
        self.assertEqual(self.post.text, 'Filler Test body')

    def test_post_absolute_url(self):
        self.assertEqual(reverse('forumsapp:post', kwargs={'post_id': self.post.id}), self.post.get_absolute_url)

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
        self.assertEqual(self.comment.text, 'test body')
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
        self.assertEqual(self.post.downvote_count, 0)

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
