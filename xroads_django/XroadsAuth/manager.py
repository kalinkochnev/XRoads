from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, authenticate
from allauth.account.models import EmailAddress

class CustomUserManager(BaseUserManager):
    """This custom user manager uses email as the unique identifiers for authentication instead of usernames.
    The manager deals with user management functionality (creation, deletion, modification etc)
    This is a custom manager that extends from BaseUserManager which is a stripped down version of django's default
    user manager that comes with it by default"""

    # Get a User with the given email
    def login(self, email, password):
        if not email:
            raise ValueError(_('The email must be set'))
        if not password:
            raise ValueError(_('The password must be set'))
        user = authenticate(username=email, password=password)
        return user

    # Create and save a User with the given email and password, automatically generate a tag
    def create_user(self, email, password, **extra_fields):

        # tests that the given parameters have values that fall in given constraints
        if not email:
            raise ValueError(_('The email must be set'))
        if not password:
            raise ValueError(_('The password must be set'))

        # formats email address, creates user model object
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # sets the password using a method on the model (more secure with hashing) and save the changes
        user.set_password(password)
        user.save(using=self._db)

        # TEST Probably difficult to test. Used for django allauth
        EmailAddress.objects.create(user=user, email=user.email, verified=False, primary=True)

        return user

    # Create and save a superuser with the given email and password. Is already verified
    def create_superuser(self, email, password, **extra_fields):
        """extra_fields is a dictionary that can be iterated through for additional parameters to be entered that aren't
        directly list above. This sets these key and value pairs as true because the user has super status"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # makes sure that the key and values of extra_fields set correctly
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Super user must have is_staff = True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True'))

        # creates a user using parameters given and extra fields provides superuser status
        user = self.create_user(email, password, **extra_fields)

        # TEST Probably difficult to test. Used for django allauth
        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)

        return user

    # Use default authentication method for login
    def signup(self, email, password):
        User = get_user_model()
        # create a user if no users with the same email exist. Email is already validated by the form
        try:
            user = User.objects.get(email=email)
            return None
        except User.DoesNotExist:
            user = self.create_user(email=email, password=password)
            return user