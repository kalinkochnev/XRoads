import datetime
from XroadsAPI.tasks import weekly_task
from django.db import models
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models import Q

from XroadsAPI.slides import get_slide_urls
import random
import xkcdpass.xkcd_password as xp


class Club(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    img = models.ImageField()
    is_visible = models.BooleanField(default=False)
    presentation_url = models.URLField()
    contact = models.EmailField(blank=True, null=True)
    featured_order = models.IntegerField(blank=True, null=True, default=None)

    extra_info = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=30, blank=True)

    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True)

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
    def district(self):
        return self.school.district

    @property
    def slides(self):
        return get_slide_urls(self.presentation_url)

    def send_extra_info(self, email):
        subject, from_email, to = f'Extra info for {self.name}', settings.DJANGO_NO_REPLY, [
            email]

        send_mail(subject, self.extra_info, from_email, to)

    def save(self, *args, **kwargs):
        if not self.pk and not self.code:
            self.code = self.gen_code()

        if self.school is not None and self.featured_order is None:
            self.featured_order = self.school.clubs.count() + 1

        super(Club, self).save(*args, **kwargs)

    @property
    def events(self):
        events_gt_today = Q(date__gt=datetime.date.today())
        today_unfinished_events = Q(end__gte=datetime.datetime.now(), date=datetime.date.today()) 
        return Event.objects.filter(today_unfinished_events | events_gt_today, club=self)

class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    name = models.CharField(max_length=35)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    requested_count = models.IntegerField(default=0)

class School(models.Model):
    name = models.CharField(max_length=40)
    img = models.ImageField()
    district = models.ForeignKey(
        'District', on_delete=models.CASCADE, null=True)

    featured: Club = models.ForeignKey(
        Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='featured')

    club_contact = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - id: {self.id}"

    def make_save(self, save):
        if save:
            self.save()

    def add_club(self, club: Club, save=True):
        club.school = self
        club.make_save(save)

    @property
    def clubs(self):
        return Club.objects.filter(school=self)

    @property
    def curr_featured_order(self):
        if self.featured is not None:
            return self.featured.featured_order
        return 0

    @property
    def next_featured(self):
        return self.get_next()

    def email_club_warning(self, club: Club):
        if club is None:
            return

        contact = club.contact

        if self.club_contact and contact is not None:
            subject, from_email, to = f'{club.name} is going to be featured!', settings.DJANGO_NO_REPLY, [
                contact]
            plain_text = get_template('email/featured_alert.txt')

            text_content = plain_text.render({'club': club, 'school': self})

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.send()

    def email_featured(self, club: Club):
        if club is None:
            return

        club_contact = club.contact
        if self.club_contact and club_contact is not None:
            subject, from_email, to = f'{club.name} is being featured right now!', settings.DJANGO_NO_REPLY, [
                club_contact]
            plain_text = get_template('email/curr_featured.txt')

            text_content = plain_text.render({'club': club, 'school': self})

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.send()

    # If you specify a start position, it gets the next club from that position
    def get_next(self, start=None):
        curr_id = 0

        if start is not None:
            curr_id = start
        elif self.featured is not None:
            curr_id = self.featured.featured_order

        try:
            return Club.objects.get(featured_order=curr_id + 1, school=self)
        except Club.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        if self.pk:
            if self.featured is None:
                self.featured = self.get_next()
                self.email_featured(self.featured)
                self.email_club_warning(self.next_featured)

        super(School, self).save(*args, **kwargs)

# Scheduling every monday at 8 am
@weekly_task(week_day=0, hours=23, minutes=59)
def update_featured_club():
    school: School
    for school in School.objects.all():
        school.featured = school.get_next()
        school.save()
    print('updated school')


class DistrictDomain(models.Model):
    domain = models.CharField(max_length=20, unique=True)
    district = models.ForeignKey(
        'XroadsAPI.District', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.district}: {self.domain}'


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

    @property
    def email_domains(self):
        return DistrictDomain.objects.filter(district=self)

    def add_email_domain(self, domain: str):
        DistrictDomain.objects.create(domain=domain, district=self)

    def remove_email_domain(self, domain: str):
        try:
            district_domain = DistrictDomain.objects.get(
                domain=domain, district=self)
            district_domain.delete()
        except DistrictDomain.DoesNotExist:
            pass

    @classmethod
    def match_district(cls, email):
        domain = email.split('@')[1]
        yo = 1

        try:
            return DistrictDomain.objects.get(domain=domain).district
        except DistrictDomain.DoesNotExist:
            return None
