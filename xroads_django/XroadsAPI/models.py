from django.core.exceptions import FieldError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re

from XroadsAPI.exceptions import *

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
            raise FieldError(
                'The phone number provided must have len of 10 and include the area code')

        return parsed

    @classmethod
    def create_profile(cls, email, password, first, last, phone='', is_anon=False):
        user = User.objects.create(
            email=email, first_name=first, last_name=last)
        user.set_password(password)

        phone = None if phone == '' else cls.parse_phone(phone)
        return Profile.objects.create(user=user, phone=phone, is_anon=is_anon)


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
    def new_slide(cls, temp_id, **kwargs:dict) -> Slide:
        template = SlideTemplates.get(temp_id)

        if template.args_match(kwargs.keys()):
            return Slide.objects.create(template_type=temp_id, **kwargs)
        raise SlideParamError(
            f'Args given do not match. Expected args: {template.required_args} Given: {kwargs} ')


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()


class MeetDay(models.Model):
    class Day(models.TextChoices):
        MONDAY = 'MONDAY',
        TUESDAY = 'TUESDAY',
        WEDNESDAY = 'WEDNESDAY',
        THURSDAY = 'THURSDAY',
        FRIDAY = 'FRIDAY',
        SATURDAY = 'SATURDAY',
        SUNDAY = 'SUNDAY',
        CUSTOM = 'CUSTOM',

    day = models.CharField(max_length=15, choices=Day.choices)


class Club(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    main_img = models.ImageField()

    meeting_days = models.ManyToManyField(MeetDay)
    commitment = models.CharField(max_length=10)
    faq = models.ManyToManyField(Faq)

    members = models.ManyToManyField(Profile)
    slides = models.ManyToManyField(Slide)
    is_visible = models.BooleanField()

    def add_meet_day(self, day: MeetDay.Day):
        day, created = MeetDay.objects.get_or_create(day=day)

    def remove_meet_day(self, day: MeetDay.Day):
        day = self.meeting_days.get(day=day).delete()

    def add_faq_question(self, question, answer):
        new_faq = Faq.objects.create(question=question, answer=answer)
        self.faq.add(new_faq)

    def remove_faq_question(self, question_id):
        self.faq.remove(id=question_id)

