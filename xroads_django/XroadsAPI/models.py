from django.db import models
from django.db.models.expressions import Random
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from XroadsAPI.slides import get_slides
import random


class Club(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    img = models.ImageField()
    is_visible = models.BooleanField(default=False)
    presentation_url = models.URLField()
    contact = models.EmailField(blank=True, null=True)

    hidden_info = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=30)

    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True)

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
        return get_slides(self.presentation_url)


class School(models.Model):
    name = models.CharField(max_length=40)
    img = models.ImageField()
    district = models.ForeignKey(
        'District', on_delete=models.CASCADE, null=True)

    club_contact = models.BooleanField(default=False)
    _curr_club: Club = models.ForeignKey(
        Club, null=True, on_delete=models.SET_NULL, related_name="curr_club", blank=True)
    _next_club: Club = models.ForeignKey(
        Club, null=True, on_delete=models.SET_NULL, related_name="next_club", blank=True)

    featured = models.ManyToManyField(
        Club, related_name="featured_club", blank=True)

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

    def get_unfeatured(self) -> Club:
        not_featured = self.clubs.difference(self.featured.all())

        if not_featured.count() > 0:
            return random.choice(not_featured)
        return None

    def get_next(self, save=True):
        if self.next_club is None:
            self.next_club = self.get_unfeatured()

        self.curr_club = self.next_club
        self.next_club = self.get_unfeatured()

        if save:
            self.save()

    @property
    def curr_club(self):
        return self._curr_club

    @curr_club.setter
    def curr_club(self, value):
        self._curr_club = value

        if self._curr_club is not None:
            self.featured.add(self._curr_club)

    @property
    def next_club(self):
        return self._next_club

    @next_club.setter
    def next_club(self, value):
        self._next_club = value

    def email_warning(self, club: Club):
        if club is None:
            return

        contact = club.contact

        if self.club_contact and contact is not None:
            subject, from_email, to = f'{self._next_club.name} is going to be featured!', settings.DJANGO_NO_REPLY, [
                contact]
            plain_text = get_template('email/featured_alert.txt')

            text_content = plain_text.render(
                {'club': self._next_club, 'school': self})

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.send()

    def email_featured(self, club: Club):
        if club is None:
            return

        club_contact = club.contact
        if self.club_contact and club_contact is not None:
            subject, from_email, to = f'{self._curr_club.name} is being featured right now!', settings.DJANGO_NO_REPLY, [
                club_contact]
            plain_text = get_template('email/curr_featured.txt')

            text_content = plain_text.render(
                {'club': self._curr_club, 'school': self})

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.send()

    def save(self, *args, **kwargs):
        if self.pk:
            if self.curr_club is None:
                self.get_next(save=False)

            past: self = School.objects.get(id=self.id)

            if past._next_club != self._next_club:
                self.next_club = self._next_club
                self.email_warning(self._next_club)

            if past._curr_club != self._curr_club:
                self.curr_club = self._curr_club
                self.email_featured(self._curr_club)

        super(School, self).save(*args, **kwargs)


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
        try:
            return DistrictDomain.objects.get(domain=domain).district
        except DistrictDomain.DoesNotExist:
            return None
