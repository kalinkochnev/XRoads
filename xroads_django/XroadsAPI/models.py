from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    main_img = models.ImageField()
    is_visible = models.BooleanField(default=False)
    # TODO change to hidden info
    join_promo = models.TextField(blank=True, null=True)

    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True)
    # TODO store google slides link

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
    def clubs(self):
        return Club.objects.filter(school=self)


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
            district_domain = DistrictDomain.objects.get(domain=domain, district=self)
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
