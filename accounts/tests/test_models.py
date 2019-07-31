from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from accounts.models import CustomUser
import accounts.AccountModelExceptions as ModelExceptions


class UserModelTests(TestCase):
    # gets run before every method call of the test
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

        # test username attribute does not exist because it shouldn't
        try:
            self.assertIsNone(self.user.username)
        except AttributeError:
            pass

        # test when certain parameters are missing it raises the errors
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(TypeError):
            self.User.objects.create_user(alias='testuser', password='testpassword')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='norm@user.com', alias='testuser', password='')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', alias='', password='')

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

        # tests that if is_superuser=False that it raises an error
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='super@user.com', alias="superusertest", password='foo', is_superuser=False
            )

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
        # in the event that the two users have the same tag
        user1 = self.User.objects.create_user(email='email@user.com', alias='otherusername', password='testpassword')
        user2 = self.User.objects.create_user(email='diffemail@user.com', alias='otherusername', password='testpassword')
        user1.user_tag = 5000
        user2.user_tag = 5000
        user1.update_user()
        user2.update_user()

        # make sure that in given cases these exceptions are raised
        with self.assertRaises(ModelExceptions.TagTaken):
            user1.validate_tag(5000)
        with self.assertRaises(ModelExceptions.TagTaken):
            user2.validate_tag(5000)
        with self.assertRaises(ModelExceptions.NoAvailableTags):
            user1.validate_tag(5000, taken_tags=range(1000, 10000))
        with self.assertRaises(ModelExceptions.OutOfBounds):
            user1.validate_tag(99999)

    def test_authentication(self):
        # check that auth returns a user object that is the expected one
        user_email = 'email@user.com'
        user_password = 'testpassword'
        user1 = self.User.objects.create_user(email=user_email, alias='otherusername', password=user_password)
        returned_user = authenticate(email=user_email, password=user_password)
        self.assertEqual(user1, returned_user)

        # check that None is returned if password is incorrect
        user_email = 'email@user.com'
        user_wrong_password = 'yikes'
        user2 = self.User.objects.create_user(email='email2@user.com', alias='otherusername', password='testpassword')
        returned_user = authenticate(email=user_email, password=user_wrong_password)
        self.assertIsNone(returned_user)

    def test_signup(self):
        # should return a user object since it doesn't exist
        user_email = 'new@email.com'
        user_pass = 'somepass'
        user_alias = 'testuser'
        new_user = self.User.objects.signup(user_email, user_alias, user_pass)
        self.assertEqual(new_user.email, user_email)
        self.assertTrue(new_user.check_password(user_pass))
        self.assertEqual(new_user.alias, user_alias)

        # should return none since user with that email already exists
        other_user = self.User.objects.signup(user_email, 'blah', 'password')
        self.assertIsNone(other_user)
