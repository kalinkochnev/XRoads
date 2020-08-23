import pytest
from XroadsAPI.models import *
from XroadsAuth.models import Profile
from django.db import IntegrityError

def test_match_email_with_district(create_test_prof):
    d1: District = District.objects.create(name='d1')
    prof: Profile = create_test_prof(1)

    assert prof.district == None

    prof.email = "test_email@school.org"
    prof.save()

    domain = d1.add_email_domain('school.org')

    prof.match_district()
    assert prof.district == d1
    
def test_domain_already_created(db):
    d1: District = District.objects.create(name='d1')
    domain1 = DistrictDomain.objects.create(domain='school.org', district=d1)

    # Test with same district
    with pytest.raises(IntegrityError):
        assert d1.add_email_domain('school.org')

def test_domain_already_created_other_district(db):
    d1: District = District.objects.create(name='d1')
    domain1 = DistrictDomain.objects.create(domain='school.org', district=d1)

    # Test with different district

    d2: District = District.objects.create(name='d2')
    with pytest.raises(IntegrityError):
        assert d2.add_email_domain('school.org')
        

