from django.core.exceptions import FieldError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=True, blank=True)
    is_anon = models.BooleanField()

    @property
    def phone_num(self):
        return None if self.phone is None else int(self.phone)

    @staticmethod
    def parse_phone(input_str):
        parsed = re.sub('[^0-9]', '', input_str)

        if len(parsed) != 10:
            raise FieldError('The phone number provided must have len of 10 and include the area code')

        return parsed

    @classmethod
    def create_profile(cls, email, password, first, last, phone='', is_anon=False):
        user = User.objects.create(email=email, first_name=first, last_name=last)
        user.set_password(password)

        phone = None if phone == '' else cls.parse_phone(phone)
        return Profile.objects.create(user=user, phone=phone, is_anon=is_anon)

"""
class Slide(models.Model):
    position = models.IntegerField()
    video_url = models.URLField(blank=True)
    img = models.ImageField(blank=True)
    text = models.TextField(max_length=500, blank=True)
    template_type = models.IntegerField()

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()


class Club(models.Model):
    members = models.ManyToManyField(to=Profile)
    name = models.CharField(max_length=30)
    slides = models.ManyToManyField(Slide)

    class MeetDays(models.TextChoices):
        MONDAY = 'MONDAY',
        TUESDAY = 'TUESDAY',
        WEDNESDAY = 'WEDNESDAY',
        THURSDAY = 'THURSDAY',
        FRIDAY = 'FRIDAY',
        SATURDAY = 'SATURDAY',
        SUNDAY = 'SUNDAY',
        CUSTOM = 'CUSTOM',

    meeting_days = models.CharField(max_length=15, choices=MeetDays.choices, default=MeetDays.CUSTOM)
    commitment = models.CharField(max_length=10)
    faq = models.ManyToManyField(FAQ)
    is_visible = models.BooleanField()

    main_img = models.ImageField()

"""
