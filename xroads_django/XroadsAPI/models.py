from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from django.dispatch import receiver

from XroadsAPI.exceptions import *
from XroadsAuth.manager import CustomUserManager
from XroadsAuth.models import Profile
import XroadsAPI.slide as SlideTemp


class Slide(models.Model):
    class Meta:
        ordering = ['position']

    club = models.ForeignKey('Club', on_delete=models.CASCADE)

    position = models.IntegerField()
    template_type = models.IntegerField()

    video_url = models.URLField(blank=True, null=True)
    img = models.ImageField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    @property
    def template(self):
        return SlideTemp.SlideTemplates.get(temp_id=self.template_type)

    def __str__(self):
        return f"{self.club} slide {self.position} {self.template.name}"


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

    def __str__(self):
        return f"{self.day} id: {self.id}"


class Club(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    main_img = models.ImageField()
    hours = models.CharField(max_length=10)
    is_visible = models.BooleanField(default=False)

    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True)

    meeting_days = models.ManyToManyField(MeetDay, blank=True)
    members = models.ManyToManyField(Profile, blank=True)

    def __str__(self):
        return self.name

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
        new_slide = SlideTemp.SlideTemplates.new_slide(
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

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name

    def add_school(self, school: School):
        school.district = self
        school.make_save(True)

    @property
    def schools(self):
        return School.objects.filter(district=self)
