from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
import accounts.AccountModelExceptions as ModelExceptions

class UserModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='norm@user.com', alias='testuser', password='testpassword')

    def test_norm_user_creation(self):

        self.assertEqual(self.user.email, 'norm@user.com')
        self.assertEqual(self.user.alias, 'testuser')
        # TODO Test when the user has the same username and tag that the tag becomes different
        self.assertIsNotNone(self.user.user_tag)
        self.assertEqual(f'{self.user.alias}#{self.user.user_tag}', self.user.__str__())

        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

        # test username attribute does not exist
        try:
            self.assertIsNone(self.user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(TypeError):
            self.User.objects.create_user(alias='testuser', password='testpassword')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='norm@user.com', alias='testuser', password='')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', alias='', password='')

    def test_tag_creation(self):
        user2 = self.User.objects.create_user(email='normal@user.com', alias='otherusername', password='testpassword')

        # tags should be generated
        self.assertIsNotNone(self.user.user_tag)
        self.assertIsNotNone(user2.user_tag)

        # user tags should not match
        self.assertNotEqual(self.user.user_tag, user2.user_tag)
        # emails should not match
        self.assertNotEqual(self.user.email, user2.email)

    def test_tag_validation(self):
        user1 = self.User.objects.create_user(email='email@user.com', alias='otherusername', password='testpassword')
        user2 = self.User.objects.create_user(email='diffemail@user.com', alias='otherusername', password='testpassword')
        user1.user_tag = 5000
        user2.user_tag = 5000
        user1.update_tag()
        user2.update_tag()

        with self.assertRaises(ModelExceptions.TagTaken):
            user1.validate_tag(5000)
        with self.assertRaises(ModelExceptions.TagTaken):
            user2.validate_tag(5000)
        with self.assertRaises(ModelExceptions.NoAvailableTags):
            user1.validate_tag(5000, taken_tags=range(1000, 10000))
        with self.assertRaises(ModelExceptions.OutOfBounds):
            user1.validate_tag(99999)

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(email='super@user.com', alias='superusertest', password='foo')
        self.assertEquals(admin_user.email, 'super@user.com')
        self.assertEquals(admin_user.alias, 'superusertest')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        # test username attribute does not exist
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass

        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='super@user.com', alias="superusertest", password='foo', is_superuser=False
            )
