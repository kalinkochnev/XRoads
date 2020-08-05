from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from django.dispatch import receiver

from XroadsAPI.exceptions import *
from XroadsAuth.manager import CustomUserManager
from XroadsAuth.models import Profile



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
        return School.objects.get(clubs__in=[self])

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

    @property
    def district(self):
        return District.objects.get(schools__in=[self])

class District(models.Model):
    schools = models.ManyToManyField(School)
    name = models.CharField(max_length=40)

    def add_school(self, school):
        self.schools.add(school)