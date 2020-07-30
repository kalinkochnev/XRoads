from django.core.exceptions import FieldError
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django.dispatch import receiver
import re

from XroadsAPI.exceptions import *
from XroadsAPI.manager import CustomUserManager


class HierarchyPerms(models.Model):
    perm_name = models.CharField(max_length=200)

class Profile(AbstractUser):
    """User model that uses email instead of username."""
    email = models.EmailField(_('email address'), unique=True)
    username = None

    # used for making sure the admin login and signup page works correctly
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Brings in the CustomUserManager we made so we can use all its methods
    objects = CustomUserManager()

    # Everything past this point is not related to the custom user model
    phone = models.CharField(max_length=10, null=True, blank=True)
    is_anon = models.BooleanField(default=False)

    hierachy_perms = models.ManyToManyField(HierarchyPerms)

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
        school.students.add(self)
        school.save()
        self.make_save(save)

    @property
    def school(self):
        return School.objects.get(students__in=[self])

    def make_editor(self, club):
        assert club.school == self.school, "You can't make somebody the editor of a club they aren't in"

    def add_perm(self, perm):
        self.hierachy_perms.add(perm)
        self.make_save(save=True)

class Slide(models.Model):
    class Meta:
        ordering = ['position']

    position = models.IntegerField()
    template_type = models.IntegerField()

    video_url = models.URLField(blank=True, null=True)
    img = models.ImageField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)


class SlideTemplates:
    class Template:
        possible_args = ['img', 'text', 'video_url']

        def __init__(self, temp_id: int, name, required):
            self.temp_id = temp_id

            # makes sure that position is always included
            self.required_args = required
            self.required_args.append('position')

            self.name = name

        def args_match(self, args):
            return set(args) == set(self.required_args)

    templates = [
        Template(temp_id=1, name="img/text",  required=['img', 'text']),
        Template(temp_id=2, name="img_only", required=['img']),
        Template(temp_id=3, name="video_only", required=['video_url']),
    ]

    @classmethod
    def get(cls, temp_id: int):
        for temp in cls.templates:
            if temp.temp_id == temp_id:
                return temp
        raise InvalidSlideTemplate(
            'The specified template type does not exist')

    @classmethod
    def new_slide(cls, temp_id, **kwargs: dict) -> Slide:
        template = SlideTemplates.get(temp_id)

        if template.args_match(kwargs.keys()):
            return Slide.objects.create(template_type=temp_id, **kwargs)
        raise SlideParamError(
            f'Args given do not match. Expected args: {template.required_args} Given: {kwargs} ')


class MeetDay(models.Model):
    class Day(models.TextChoices):
        MONDAY = 'MONDAY'
        TUESDAY = 'TUESDAY'
        WEDNESDAY = 'WEDNESDAY'
        THURSDAY = 'THURSDAY'
        FRIDAY = 'FRIDAY'
        SATURDAY = 'SATURDAY'
        SUNDAY = 'SUNDAY'
        CUSTOM = 'CUSTOM'

    day = models.CharField(
        max_length=15, choices=Day.choices, default=Day.CUSTOM)


class Club(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    main_img = models.ImageField()
    hours = models.CharField(max_length=10)
    is_visible = models.BooleanField(default=False)

    meeting_days = models.ManyToManyField(MeetDay, blank=True)
    members = models.ManyToManyField(Profile, blank=True)
    slides = models.ManyToManyField(Slide, blank=True)

    def make_save(self, save):
        if save:
            self.save

    def add_meet_day(self, day: MeetDay.Day, save=True) -> MeetDay:
        day, created = MeetDay.objects.get_or_create(day=day)
        if created:
            self.meeting_days.add(day)
            self.make_save(save)
        return day

    def remove_meet_day(self, day: MeetDay.Day, save=True):
        self.meeting_days.remove(self.meeting_days.get(day=day))
        self.make_save(save)

    def add_slide(self, template_type, save=True, **kwargs) -> Slide:
        max_pos = self.slides.count()
        new_slide = SlideTemplates.new_slide(
            template_type, position=max_pos+1, **kwargs)
        self.slides.add(new_slide)
        self.make_save(save)
        return new_slide

    def remove_slide(self, position, save=True):
        self.slides.remove(self.slides.get(position=position))
        self.make_save(save)

    def join(self, profile: Profile, save=True):
        self.members.add(profile)
        self.make_save(save)

    def leave(self, profile: Profile, save=True):
        self.members.remove(profile)
        self.make_save(save)

    def toggle_hide(self, save=True):
        self.is_visible = not self.is_visible
        self.make_save(save)

    # TODO add test for this
    @property
    def school(self):
        return School.objects.get(clubs=[self])

# TODO make clubs many to one
class School(models.Model):
    name = models.CharField(max_length=40)
    img = models.ImageField()
    clubs = models.ManyToManyField(Club)
    students = models.ManyToManyField(Profile)

    def make_save(self, save):
        if save:
            self.save()

    def add_club(self, club: Club, save=True):
        self.clubs.add(club)
        self.make_save(save)

class District(models.Model):
    schools = models.ManyToManyField(School)
    name = models.CharField(max_length=40)

    def add_school(self, school):
        self.schools.add(school)