import pytest
from XroadsAPI.models import School

def test_join_school(create_test_prof):
    school = School.objects.create(name="Some School")
    prof = create_test_prof(1)
    prof.join_school(school)
    assert school.students.count() == 1

    # Test school property in profile class
    assert school == prof.school
