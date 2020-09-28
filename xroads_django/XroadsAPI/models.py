from django.db import models

import XroadsAPI.slide as SlideTemp
from XroadsAPI.exceptions import *
import XroadsAuth.models as AuthModels


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


class Club(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    main_img = models.ImageField()
    hours = models.CharField(max_length=10)
    is_visible = models.BooleanField(default=False)
    join_promo = models.TextField(blank=True, null=True)

    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True)

    members = models.ManyToManyField('XroadsAuth.Profile', blank=True)

    def __str__(self):
        return f"{self.name} - id: {self.id}"

    def make_save(self, save):
        if save:
            self.save()


    def add_slide(self, template_type, save=True, **kwargs) -> Slide:
        max_pos = self.slides.count()
        new_slide = SlideTemp.SlideTemplates.new_slide(
            template_type, club=self, position=max_pos+1, **kwargs)
        self.make_save(save)
        return new_slide

    def remove_slide(self, position, save=True):
        self.slides.filter(position=position).delete()
        self.make_save(save)

    def join(self, profile, save=True):
        self.members.add(profile)
        self.make_save(save)

    def leave(self, profile, save=True):
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

    @property
    def editors(self):
        import XroadsAuth.permissions as AuthPerms
        club_role = AuthPerms.Role.from_start_model(self)
        # FIXME make sure it works with more than one role model
        
        return AuthModels.Profile.objects.filter(roles__role_name=club_role.role_str)

class School(models.Model):
    name = models.CharField(max_length=40)
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
    def students(self):
        return AuthModels.Profile.objects.filter(school=self)

    @property
    def clubs(self):
        return Club.objects.filter(school=self)

class DistrictDomain(models.Model):
    domain = models.CharField(max_length=20, unique=True)
    district = models.ForeignKey('XroadsAPI.District', on_delete=models.CASCADE)

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
            domain = DistrictDomain.objects.get(domain=domain, district=self)
            domain.delete()
        except DistrictDomain.DoesNotExist:
            pass

    @classmethod
    def match_district(cls, email):
        domain = email.split('@')[1]
        try:
            return DistrictDomain.objects.get(domain=domain).district
        except DistrictDomain.DoesNotExist:
            return None

class Question(models.Model):
    asker = models.ForeignKey('XroadsAuth.Profile', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    question = models.TextField()
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question
