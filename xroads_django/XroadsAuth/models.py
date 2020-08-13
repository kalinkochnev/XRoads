from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from XroadsAuth.manager import CustomUserManager 
import re
from allauth.account.models import EmailAddress
from django.core.exceptions import FieldError
import XroadsAPI.models as api_models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here

class HierarchyPerms(models.Model):
    perm_name = models.CharField(max_length=200)

class Profile(AbstractUser):
    """User model that uses email instead of username."""
    email = models.EmailField(_('email address'), unique=True)
    username = None

    # Refactor Manually 
    school = models.ForeignKey('XroadsAPI.School', on_delete=models.SET_NULL, null=True) # UNTESTED 

    # used for making sure the admin login and signup page works correctly
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Brings in the CustomUserManager we made so we can use all its methods
    objects = CustomUserManager()

    # Everything past this point is not related to the custom user model
    phone = models.CharField(max_length=10, null=True, blank=True)
    is_anon = models.BooleanField(default=False)

    hierarchy_perms = models.ManyToManyField(HierarchyPerms)

    def make_save(self, save):
        if save:
            self.save()

    @property
    def phone_num(self):
        return None if self.phone is None else int(self.phone)

    @phone_num.setter
    def phone_num(self, val: int):
        self.phone = str(val)
        self.make_save(save=True)

    @staticmethod
    def parse_phone(input_str):
        parsed = re.sub('[^0-9]', '', input_str)

        if len(parsed) != 10:
            raise FieldError(
                'The phone number provided must have len of 10 and include the area code')

        return parsed

    @classmethod
    def create_profile(cls, email, password, first, last, phone='', is_anon=False):
        phone = None if phone == '' else cls.parse_phone(phone)

        return cls.objects.create_user(email=email, first_name=first, last_name=last, password=password, phone=phone, is_anon=is_anon)

    def join_school(self, school, save=True):
        self.school = school
        self.make_save(save)

    def make_editor(self, club):
        assert club.school == self.school, "You can't make somebody the editor of a club they aren't in"

    def add_perm(self, perm):
        self.hierarchy_perms.add(perm)
        self.make_save(save=True) 

    def verify(self):
        email = EmailAddress.objects.get_for_user(self, self.email)