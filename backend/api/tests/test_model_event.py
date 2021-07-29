from datetime import timedelta
import pytest
from unittest import mock
import datetime as dt
from api.models import *

@pytest.fixture
def create_event():
    def create(club, date, start, **kwargs):
        end_time = dt.datetime.combine(date.today(), start) + timedelta(**kwargs)
        data = {
            'name': 'event1',
            'description': 'description',
            'views': 1,
            'end': end_time.time(),
            'start': start,
            'date': date,
            'club': club,
        }

        return Event.objects.create(**data) 
    return create

def test_filter_events(create_club, create_event):
    club: Club = create_club()
    todays_date = dt.datetime(2020, 12, 1) # current date is December 1st 2020
    current_time = dt.time(hour=13, minute=0, second=0) # current time is 1pm
    real_dt = dt.datetime

    prev_event = create_event(club=club, date=todays_date - dt.timedelta(days=1), start=current_time, hours=1) 
    todays_event = create_event(club=club, date=todays_date, start=current_time, hours=1)
    later_event = create_event(club=club, date=todays_date + dt.timedelta(days=1), start=current_time, hours=1)

    with mock.patch('api.models.datetime') as mock_date:
        mock_date.datetime.return_value = real_dt
        mock_date.date.today.return_value = todays_date
        mock_date.datetime.now.return_value = current_time

        events = club.events
        assert todays_event in events
        assert later_event in events
        assert prev_event not in events