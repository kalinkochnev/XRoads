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

    club = models.ForeignKey('Club', on_delete=models.CASCADE)

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
    def new_slide(cls, temp_id, club, **kwargs: dict) -> Slide:
        template = SlideTemplates.get(temp_id)

        if template.args_match(kwargs.keys()):
            return Slide.objects.create(club=club, template_type=temp_id, **kwargs)
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

    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True)

    meeting_days = models.ManyToManyField(MeetDay, blank=True)
    members = models.ManyToManyField(Profile, blank=True)

    def make_save(self, save):
        if save:
            self.save()

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
            template_type, club=self, position=max_pos+1, **kwargs)
        self.make_save(save)
        return new_slide

    def remove_slide(self, position, save=True):
        self.slides.filter(position=position).delete()
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

    @property
    def slides(self):
        return Slide.objects.filter(club=self)

    @property
    def district(self):
        return self.school.district

class School(models.Model):
    name = models.CharField(max_length=40)
    img = models.ImageField()
    district = models.ForeignKey(
        'District', on_delete=models.CASCADE, null=True)

    def make_save(self, save):
        if save:
            self.save()

    def add_club(self, club: Club, save=True):
        club.school = self
        club.make_save(save)

    @property
    def students(self):
        return Profile.objects.filter(school=self)

    @property
    def clubs(self):
        return Club.objects.filter(school=self)


class District(models.Model):
    name = models.CharField(max_length=40)

    def add_school(self, school: School):
        school.district = self
        school.make_save(True)

    @property
    def schools(self):
        return School.objects.filter(district=self)
