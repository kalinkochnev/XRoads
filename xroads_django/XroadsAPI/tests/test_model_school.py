from XroadsAPI.slides import create_credentials
import pytest
from typing import Callable, Iterable
from django.core import mail
from django.conf import settings

from XroadsAPI.models import Club, District, School


class TestSchool:
    def test_init_school_with_featured_clubs(self, role_model_instances, create_club, db):
        # 1 club
        s1: School = School.objects.create(name="s1")
        assert s1.curr_club is None
        assert s1.next_club is None

        c1 = create_club()
        s1.add_club(c1)
        s1.save()
        assert s1.curr_club == c1

    def test_init_school_2_clubs(self, create_club):
        s2: School = School.objects.create(name="s2")
        assert s2.curr_club is None
        assert s2.next_club is None

        c1 = create_club()
        c2 = create_club()

        s2.add_club(c1)
        s2.add_club(c2)
        s2.save()
        assert s2.curr_club is not None
        assert s2.next_club is not None
        assert s2.curr_club != s2.next_club

    def test_featured_email_sent(self, create_club):
        s1: School = School.objects.create(name="s1")
        assert s1.curr_club is None
        assert s1.next_club is None

        c1: Club = create_club()
        c1.contact = "test@email.com"

        s1.add_club(c1)
        s1.curr_club = c1
        s1.club_contact = True

        assert s1.curr_club == c1
        s1.save()

        assert c1 in list(s1.featured.all())
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == f'{c1.name} is being featured right now!'
        assert mail.outbox[0].from_email == settings.DJANGO_NO_REPLY
        assert mail.outbox[0].to == ["test@email.com"]

    @pytest.mark.skip("Not super useful to test")
    def test_featured_warning_sent(self, create_club):
        s1: School = School.objects.create(name="s1")
        assert s1.curr_club is None
        assert s1.next_club is None

        c1: Club = create_club()
        c1.contact = "test@email.com"

        s1.add_club(c1)
        s1.add_club(c1)

        s1.next_club = c1
        s1.club_contact = True
        assert s1.next_club == c1
        s1.save()

        assert len(mail.outbox) == 2
        assert mail.outbox[0].subject == f'{c1.name} is going to be featured!'
        assert mail.outbox[0].from_email == settings.DJANGO_NO_REPLY
        assert mail.outbox[0].to == ["test@email.com"]

    def test_set_curr_club(self, create_club):
        s1: School = School.objects.create(name="s2")
        c1 = create_club()
        c1.contact = "test@email.com"
        c1.save()

        s1.add_club(c1, save=False)
        s1.club_contact = True
        s1.save()

        assert s1.featured.all().count() == 0
        s1.curr_club = c1

    def test_set_next_club(self, role_model_instances):
        d1, s1, c1 = role_model_instances()
        c1.contact = "test@email.com"
        c1.save()

        s1.club_contact = True
        s1.save()
        
        s1.next_club = c1

    def test_get_next_featured(self, role_model_instances, create_club):
        d1, s1, c1 = role_model_instances()
        s1: School
        clubs = [c1] + [s1.add_club(create_club()) for i in range(1, 3)]

        s1.curr_club = clubs[0]
        s1.next_club = clubs[1]
        s1.get_next()
        assert s1.featured is not None

    def test_get_next_clubs_exist(self, create_club):
        school = School.objects.create(name="s")

        clubs = [create_club(id=i) for i in range(3)]
        for c in clubs:
            school.add_club(c)

        assert school.curr_club is None
        assert school.next_club is None

        school.save()

        assert school.curr_club is not None
        assert school.next_club is not None
        assert school.next_club != school.curr_club

    def test_get_next_1_club_exist(self, role_model_instances):
        d1, s1, c1 = role_model_instances()

        assert s1.curr_club is None
        assert s1.next_club is None

        s1.save()

        assert s1.curr_club is not None
        assert s1.next_club is None
