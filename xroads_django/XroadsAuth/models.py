from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.dispatch import receiver
from django.template.loader import get_template

from XroadsAuth.manager import CustomUserManager
import XroadsAPI.models as APIModels

# Create your models here


class RoleModel(models.Model):
    role_name = models.CharField(max_length=200)
    perms = ArrayField(base_field=models.CharField(max_length=50))

    @classmethod
    def from_role(cls, role):
        role, created = cls.objects.get_or_create(
            role_name=role.role_str, perms=list(role.permissions.permissions))
        return role

    @classmethod
    def get_role(cls, role):
        return cls.objects.get(role_name=role.role_str, perms=list(role.permissions.permissions))

    def __str__(self):
        return str(self.role)

    @property
    def role(self):
        from .permissions import Role
        return Role.from_str(self.role_name, perms=self.perms)

    @property
    def highest_level_str(self):
        # This creates a string in the format of [highest_level]/perms=[]  ex School-1/perms=[]
        return '/'.join(str(self.role).split("/")[-2:])


class Profile(AbstractUser):
    """User model that uses email instead of username."""
    email = models.EmailField(_('email address'), unique=True)
    username = None

    school = models.ForeignKey(
        'XroadsAPI.School', on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(
        'XroadsAPI.District', on_delete=models.SET_NULL, null=True)

    # used for making sure the admin login and signup page works correctly
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Brings in the CustomUserManager we made so we can use all its methods
    objects = CustomUserManager()

    # Everything past this point is not related to the custom user model
    is_anon = models.BooleanField(default=False)

    roles = models.ManyToManyField(RoleModel, blank=True)

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

    def add_roles(self, *roles, save=True):
        self.roles.add(*roles)
        self.make_save(save)

    def remove_roles(self, *roles, save=True):
        self.roles.remove(*roles)
        self.make_save(save)

    @property
    def permissions(self):
        from .permissions import Role
        return [i.role for i in self.roles.all()]

    @property
    def simple_perm_strs(self):
        return [i.highest_level_str for i in self.permissions]

    def match_district(self, save=True):
        self.district = APIModels.District.match_district(self.email)
        self.make_save(save)


class InvitedUser(models.Model):
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(RoleModel, blank=True)

    def __str__(self):
        return self.email

    @classmethod
    def create(cls, email, roles=[]):
        from XroadsAuth.permissions import Role
        role_models = [RoleModel.from_role(r) for r in roles]
        invited = cls.objects.create(email=email)
        invited.roles.set(role_models)

        return invited

    def add_roles(self, *roles, save=True):
        self.roles.add(*roles)
        self.make_save(save)

    def remove_roles(self, *roles, save=True):
        self.roles.remove(*roles)
        self.make_save(save)

    def make_save(self, save):
        if save:
            self.save()

    @property
    def permissions(self):
        from .permissions import Role
        return [i.role for i in self.roles.all()]


@receiver(models.signals.post_save, sender=Profile)
def after_save(sender, instance, created, *args, **kwargs):
    if created:
        try:
            invited = InvitedUser.objects.get(email=instance.email)
            instance.roles.set(invited.roles.all())
            invited.delete()
        except InvitedUser.DoesNotExist:
            pass
