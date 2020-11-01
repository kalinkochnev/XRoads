from XroadsAPI.slides import create_credentials
import pytest
from typing import Callable, Iterable
from django.core import mail
from django.conf import settings

from XroadsAPI.models import Club, District, School

@pytest.fixture
def multi_clubs(create_club):
    def create_clubs(school=None, count=3):
        if school is None:
            school = School.objects.create(name)

        clubs = [create_club() for club in range(count=count)]
        school.add_club(clubs, save=False)
        school.save()
        return school, clubs
    return create_clubs

class TestSchool:
    def test_club_has_featured_order(self, multi_clubs):
        school, clubs = multi_clubs()

        expected_order = clubs.sort(lambda club: club.featured_order)
        assert len(expected_order) == 3
        saved_order = featured_order = list(school.clubs.order_by("featured_order"))
        assert expected_order == saved_order

    def test_get_next(self, multi_clubs):
        school, clubs = multi_clubs()

        prev_featured = school.featured.featured_order
        assert prev_featured == 1

        school.get_next()
        assert prev_featured != school.featured
        assert school.featured.featured_order == 2

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