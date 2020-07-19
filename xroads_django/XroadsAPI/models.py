from django.db import models
from django.contrib.auth.models import User
import re

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User)
    phone = models.IntegerField(blank=True)
    is_anon = models.BooleanField()

    def parse_phone(self, input_str):
        parsed = re.sub('[^0-9]', '', input_str)
        return int(parsed)


class Slide(models.Model):
    position = models.IntegerField()
    video_url = models.URLField(blank=True)
    img = models.ImageField(blank=True)
    text = models.TextField(max_length=500, blank=True)
    template_type = models.IntegerField()

class Club(models.Model):
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

    meeting_days = models.CharField(choices=MeetDays.choices, default=MeetDays.CUSTOM)
    commitment = models.CharField(max_length=10)
    members = models.ManyToManyField(Profile)
    faq = models.ManyToManyField(FAQ)
    is_visible = models.BooleanField()

    main_img = models.ImageField()

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
