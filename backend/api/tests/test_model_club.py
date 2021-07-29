import tempfile

import pytest

from api.models import School, District, Club

def test_add_club(db, create_club):
    club = create_club()
    school = School.objects.create(name="Some School")
    school.add_club(club)

    assert school.clubs.count() == 1
