from django.db import models
import xkcdpass.xkcd_password as xp
import random
from django.db.models import Q
import datetime
from django.utils.text import slugify
from api.slides import get_slide_urls

class Club(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=20, unique=True, null=False)

    description = models.TextField()
    code = models.CharField(max_length=30, blank=True)
    contact = models.EmailField(blank=True)
    
    img = models.ImageField()
    
    # TODO add validator for presentation url   
    presentation_url = models.URLField(validators=[])

    is_visible = models.BooleanField(default=False)

    # Generates speakable code for the club
    @classmethod
    def gen_code(cls) -> str:
        words = xp.locate_wordfile()
        word_list = xp.generate_wordlist(
            wordfile=words, min_length=4, max_length=5)
        code = xp.generate_xkcdpassword(
            wordlist=word_list, numwords=2, case='first').split(" ")
        rand_num = random.randint(10, 99)
        return "".join([code[0], str(rand_num), code[1]])

    def __str__(self):
        return f"{self.name} - id: {self.id}"

    def make_save(self, save):
        if save:
            self.save()

    def toggle_hide(self, save=True):
        self.is_visible = not self.is_visible
        self.make_save(save)

    @property
    def slides(self):
        return get_slide_urls(self.presentation_url)

    @property
    def default_slug(self):
        slugify(self.name[:20])
        return 

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.gen_code()

        if not self.slug or len(self.slug) == 0:
            self.slug = self.default_slug

        super(Club, self).save(*args, **kwargs)

    # Retrieves all events that are currently ongoing or at a later date
    @property
    def events(self):
        events_gt_today = Q(date__gt=datetime.date.today())
        today_unfinished_events = Q(
            end__gte=datetime.datetime.now(), date=datetime.date.today())
        return Event.objects.filter(today_unfinished_events | events_gt_today, club=self).order_by('date')


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    name = models.CharField(max_length=35)
    description = models.TextField()

    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f'{self.name} -- {self.club.name}: {self.club.pk}'


class School(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, unique=True, null=False)
    img = models.ImageField()
    district = models.ForeignKey(
        'District', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name} - id: {self.id}"

    def make_save(self, save):
        if save:
            self.save()

    def add_club(self, club: Club, save=True):
        club.school = self
        club.make_save(save)

    @property
    def week_events(self):
        # Get events that are going on today and up until the end of the week
        today = datetime.datetime.today()
        end_of_week = today + datetime.timedelta(days=6 - today.weekday())
        events_gt_today = Q(date__gt=datetime.date.today(),
                            date__lte=end_of_week)
        today_unfinished_events = Q(
            end__gte=datetime.datetime.now(), date=datetime.date.today())
        return Event.objects.filter(today_unfinished_events | events_gt_today, club__school=self).order_by('date')

    @property
    def clubs(self):
        return Club.objects.filter(school=self)


class District(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name} - id: {self.id}"

    def add_school(self, school: School):
        school.district = self
        school.make_save(True)

    @property
    def schools(self):
        return School.objects.filter(district=self)