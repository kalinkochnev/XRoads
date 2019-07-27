from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers for authentication instead of usernames.
    Aliases are a username that can be taken by another user but differentiated by a tag
    """

    def create_user(self, email, alias, password, **extra_fields):

        # Create and save a User with the given email and password, automatically generate a tag
        if not email:
            raise ValueError(_('The email must be set'))
        if not alias:
            raise ValueError(_('The username must be set'))
        if not password:
            raise ValueError(_('The password must be set'))
        if len(alias) > 15:
            raise ValueError(_('The username must be below 15 characters'))

        email = self.normalize_email(email)
        user = self.model(email=email, alias=alias, **extra_fields)
        user.set_password(password)
        user.new_user_save()
        return user

    def create_superuser(self, email, alias,  password, **extra_fields):
        # Create and save a superuser with the given email and password.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Super user must have is_staff = True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True'))

        return self.create_user(email, alias, password, **extra_fields)

    # TODO create test
    @staticmethod
    def authenticate(email=None, password=None):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if user.check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None

    # TODO create test
    def signup(self, email, alias, password):
        User = get_user_model()
        if not User.objects.filter(email=email).exists() and email is not None:
            # IMPORTANT make sure there is something to handle aliases with all tags taken
            user = self.create_user(email, alias, password)
            return user
        else:
            return None
