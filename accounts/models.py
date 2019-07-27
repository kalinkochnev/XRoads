from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from random import choice
from accounts.manager import CustomUserManager
from . import AccountModelExceptions
from django.utils import timezone


class CustomUser(AbstractBaseUser, PermissionsMixin):
    alias = models.CharField(max_length=15, default=None)
    email = models.EmailField(_('email address'), unique=True)
    user_tag = models.IntegerField(default=1000)
    profile_pic = models.ImageField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['alias']

    objects = CustomUserManager()

    # Gives it in the format of Username#Tag Number
    def __str__(self):
        return f"{self.alias}#{self.user_tag}"

    def set_tag(self, tag):
        self.user_tag = tag

    def validate_tag(self, tag, **testargs):
        taken_tags = set(CustomUser.objects.filter(alias=self.alias).values_list('user_tag', flat=True))
        # can specify the list response from the query for testing
        for key, value in testargs.items():
            if key == 'taken_tags':
                taken_tags = set(value)
        tag_range = set(range(1000, 10000))
        available_tags = list(tag_range - taken_tags)

        if 1000 < tag > 9999:
            raise AccountModelExceptions.OutOfBounds()
        if len(available_tags) == 0:
            raise AccountModelExceptions.NoAvailableTags()
        if tag in taken_tags:
            raise AccountModelExceptions.TagTaken()

    # Tag is guaranteed to not be repeated because of query for existing tags for alias
    def generate_unique_tag(self):
        # does not include 10000 due to range
        tag_range = set(range(1000, 10000))
        taken_tags = set(CustomUser.objects.filter(alias=self.alias).values_list('user_tag', flat=True))

        try:
            available_tag = choice(list(tag_range - taken_tags))
            self.validate_tag(available_tag)
        except AccountModelExceptions.NoAvailableTags:
            pass
        except AccountModelExceptions.OutOfBounds:
            pass
        else:
            self.user_tag = available_tag
            # TODO save the user tag when

    def update_tag(self):
        super().save(update_fields=['user_tag'])

    def new_user_save(self, *args, **kwargs):
        self.generate_unique_tag()
        super().save(*args, **kwargs)
