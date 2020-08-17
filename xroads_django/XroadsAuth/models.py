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

"""class AddRemoveAdminMixin(models.Model):
    class Meta:
        abstract = True
    
    @property
    def members(self):
        raise NotImplementedError('Must implement members property to use add/remove admin mixin')

    def add_admin(self, user: Profile, permissions):
        role = Role.from_start_model(self)



        assert permissions.issubset(role.hierarchy.) or perms == {
        }, f'The {perms} not legal for this hierarchy: {self.hierarchy.name}'

        
        

        permissions = admin_role_serializer.validated_data['permissions']
        role.permissions.add(*permissions)

        role.give_role(prof)"""
    
class Profile(AbstractUser):
    """User model that uses email instead of username."""
    email = models.EmailField(_('email address'), unique=True)
    username = None

    school = models.ForeignKey('XroadsAPI.School', on_delete=models.SET_NULL, null=True)

    # used for making sure the admin login and signup page works correctly
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Brings in the CustomUserManager we made so we can use all its methods
    objects = CustomUserManager()

    # Everything past this point is not related to the custom user model
    is_anon = models.BooleanField(default=False)

    hierarchy_perms = models.ManyToManyField(HierarchyPerms, blank=True)

    def make_save(self, save):
        if save:
            self.save()

    @classmethod
    def create_profile(cls, email, password, first, last, is_anon=False):
        return cls.objects.create_user(email=email, first_name=first, last_name=last, password=password, is_anon=is_anon)

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