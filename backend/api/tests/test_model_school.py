from api.slides import create_credentials
import pytest
from typing import Callable, Iterable
from django.core import mail
from django.conf import settings

from api.models import Club, District, School

@pytest.fixture
def multi_clubs(create_club):
    def create_clubs(school=None, count=3):
        if school is None:
            school = School.objects.create(name="s1")

        clubs = [create_club() for club in range(0, count)]
        for club in clubs:
            school.add_club(club)
        school.save()
        return school, clubs
    return create_clubs

class TestSchool:
    def test_club_has_featured_order(self, multi_clubs):
        school, clubs = multi_clubs()
        clubs.sort(key=lambda club: club.featured_order)

        expected_order = clubs
        assert len(expected_order) == 3
        saved_order = list(school.clubs.order_by("featured_order"))
        assert expected_order == saved_order

    def test_get_next(self, multi_clubs):
        school, clubs = multi_clubs()

        prev_featured = school.featured
        assert prev_featured.featured_order == 1

        next_club = school.get_next()
        assert prev_featured != next_club
        assert next_club.featured_order == 2

    def test_emails_sent(self, create_club):
        s1: School = School.objects.create(name="s1")
        assert s1.featured is None
        assert s1.next_featured is None

        c1: Club = create_club()
        c1.contact = "test@email.com"
        c2: Club = create_club()
        c2.contact = "test2@email.com"

        s1.add_club(c1)
        s1.add_club(c2)
        s1.club_contact = True
        s1.save()

        assert s1.next_featured is not None

        assert c1.featured_order == 1
        assert s1.featured == c1
        assert s1.next_featured == c2

        assert len(mail.outbox) == 2

        # Testing that the currently featured email is sent
        assert mail.outbox[0].subject == f'{c1.name} is being featured right now!'
        assert mail.outbox[0].from_email == settings.DJANGO_NO_REPLY
        assert mail.outbox[0].to == ["test@email.com"]

        # Testing that the warning email is sent
        assert mail.outbox[1].subject == f'{c2.name} is going to be featured!'
        assert mail.outbox[1].from_email == settings.DJANGO_NO_REPLY
        assert mail.outbox[1].to == ["test2@email.com"]