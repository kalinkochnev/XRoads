from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    """This custom user manager uses email as the unique identifiers for authentication instead of usernames.
    Aliases are a username that can be taken by another user but differentiated by a tag
    The manager deals with user management functionality (creation, deletion, modification etc)
    This is a custom manager that extends from BaseUserManager which is a stripped down version of django's default
    user manager that comes with it by default"""

    # Create and save a User with the given email and password, automatically generate a tag
    def create_user(self, email, alias, password, **extra_fields):

        # tests that the given parameters have values that fall in given constraints
        if not email:
            raise ValueError(_('The email must be set'))
        if not alias:
            raise ValueError(_('The username must be set'))
        if not password:
            raise ValueError(_('The password must be set'))
        if len(alias) > 15:
            raise ValueError(_('The username must be below 15 characters'))

        # formats email address, creates user model object
        email = self.normalize_email(email)
        user = self.model(email=email, alias=alias, **extra_fields)

        # sets the password using a method on the model (more secure with hashing) and save the changes
        user.set_password(password)
        user.new_user_save()
        return user

    # Create and save a superuser with the given email and password, automatically generates a tag
    def create_superuser(self, email, alias,  password, **extra_fields):
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
        return self.create_user(email, alias, password, **extra_fields)

    # Use default authentication method for login
    # TODO create tests
    def signup(self, email, alias, password):
        User = get_user_model()

        # create a user if no users with the same email exist. Email is already validated by the form
        try:
            user = User.objects.get(email=email)
            return None
        except User.DoesNotExist:
            user = self.create_user(email=email, alias=alias, password=password)
            return user
