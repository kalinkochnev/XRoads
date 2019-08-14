from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from random import choice
from accounts.manager import CustomUserManager
from . import AccountExceptions
from django.utils import timezone


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # TODO make alphanumeric requirement for alias and email
    # all the attributes of the custom user
    alias = models.CharField(max_length=15, default=None)
    email = models.EmailField(_('email address'), unique=True)
    user_tag = models.IntegerField(default=1000)
    profile_pic = models.ImageField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # used for making sure the admin login and signup page works correctly
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['alias']

    # Brings in the CustomUserManager we made so we can use all its methods
    objects = CustomUserManager()

    # When the str(User) is called it returns it in the format alias#user_tag
    def __str__(self):
        return f"{self.alias}#{self.user_tag}"

    # For changing the tag
    def set_tag(self, tag, *args, **kwargs):
        self.user_tag = tag
        # updates the model with the changes made
        self.update_user()

    def set_alias(self, newalias, *args, **kwargs):
        self.alias = newalias
        # updates the model with the changes made
        self.update_user()

    def update_user(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # makes sure the tag is valid
    def validate_tag(self, tag, **testargs):
        # creates a set from a list that was created by a query that sorts by taken tags with the same username
        taken_tags = set(CustomUser.objects.filter(alias=self.alias).values_list('user_tag', flat=True))

        # ONLY TO BE USED IN TESTING FOR EASIER ACCESS OF THE taken_tags QUERY RESULT!!!
        for key, value in testargs.items():
            if key == 'taken_tags':
                taken_tags = set(value)

        # set() uses set notation operations, basically subtracts all taken tags from all possible tags and makes a list
        tag_range = set(range(1000, 10000))
        available_tags = list(tag_range - taken_tags)

        # validates that the tag in the parameter passes certain criteria
        # Custom exceptions can be found in AccountExceptions.py
        if 1000 < tag > 9999:
            raise AccountExceptions.OutOfBounds()
        if len(available_tags) == 0:
            raise AccountExceptions.NoAvailableTags()
        if tag in taken_tags:
            raise AccountExceptions.TagTaken()

    # Tag is guaranteed to not be repeated because of query for existing tags for alias
    def generate_unique_tag(self):
        # does not include 10000 due to range function weirdness
        tag_range = set(range(1000, 10000))
        taken_tags = set(CustomUser.objects.filter(alias=self.alias).values_list('user_tag', flat=True))

        # generates unique tag using random.choice which picks value from list of available tags
        try:
            available_tag = choice(list(tag_range - taken_tags))
            self.validate_tag(available_tag)
        except AccountExceptions.NoAvailableTags:
            pass
        except AccountExceptions.OutOfBounds:
            pass
        else:
            self.user_tag = available_tag
            self.set_tag(self.user_tag)

    # when the manager calls to create a new user, it generates the tag and then saves info
    def new_user_save(self, *args, **kwargs):
        self.generate_unique_tag()
        super().save(*args, **kwargs)
