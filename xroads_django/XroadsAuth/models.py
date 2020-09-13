from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from XroadsAuth.manager import CustomUserManager
import XroadsAPI.models as APIModels

# Create your models here
class HierarchyPerms(models.Model):
    perm_name = models.CharField(max_length=200)

    def __str__(self):
        return self.perm_name

    @property
    def role(self):
        from .permissions import Role
        return Role.from_str(self.perm_name)

    @property
    def highest_level_str(self):
        # This creates a string in the format of [highest_level]/perms=[]  ex School-1/perms=[]
        return '/'.join(str(self.role).split("/")[-2:])


class Profile(AbstractUser):
    """User model that uses email instead of username."""
    email = models.EmailField(_('email address'), unique=True)
    username = None

    school = models.ForeignKey('XroadsAPI.School', on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey('XroadsAPI.District', on_delete=models.SET_NULL, null=True)

    # used for making sure the admin login and signup page works correctly
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Brings in the CustomUserManager we made so we can use all its methods
    objects = CustomUserManager()

    # Everything past this point is not related to the custom user model
    is_anon = models.BooleanField(default=False)

    hierarchy_perms = models.ManyToManyField(HierarchyPerms, blank=True)

    @property
    def joined_clubs(self):
        from XroadsAPI.models import Club
        return Club.objects.filter(members__in=[self])

    def make_save(self, save):
        if save:
            self.save()

    @classmethod
    def create_profile(cls, email, password, first, last, is_anon=False, verified=False):
        return cls.objects.create_user(email=email, first_name=first, last_name=last, password=password, is_anon=is_anon, verified=verified)

    def join_school(self, school, save=True):
        self.school = school
        self.make_save(save)

    # TODO not made
    """def make_editor(self, club):
        assert club.school == self.school, "You can't make somebody the editor of a club they aren't in"
"""
    def add_perms(self, *perms, save=True):
        self.hierarchy_perms.add(*perms)
        self.make_save(save) 

    @property
    def permissions(self):
        from .permissions import Role
        return [Role.from_str(i.perm_name) for i in self.hierarchy_perms.all()]

    @property
    def simple_perm_strs(self):
        return [i.highest_level_str for i in self.permissions]

    def match_district(self, save=True):
        self.district = APIModels.District.match_district(self.email)
        self.make_save(save)