import pytest
from django.db import IntegrityError

from XroadsAPI.models import *
from XroadsAuth.models import Profile


def test_match_email_with_district(create_test_prof):
    d1: District = District.objects.create(name='d1')
    prof: Profile = create_test_prof(1)

    assert prof.district == None

    prof.email = "test_email@school.org"
    prof.save()

    domain = d1.add_email_domain('school.org')

    prof.match_district()
    assert prof.district == d1

def test_match_email_district_no_exist(create_test_prof):
    d1: District = District.objects.create(name='d1')
    domain = d1.add_email_domain('school.org')

    prof: Profile = create_test_prof(1)

    assert prof.match_district() == None
    
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
        

def test_get_district_domains(db):
    d1: District = District.objects.create(name='d1')
    domain1 = DistrictDomain.objects.create(domain='school.org', district=d1)
    domain2 = DistrictDomain.objects.create(domain='school2.org', district=d1)
    domain3 = DistrictDomain.objects.create(domain='school3.org', district=d1)
    domains = [domain1, domain2, domain3]

    assert list(d1.email_domains) == domains

def test_remove_domain(db):
    d1: District = District.objects.create(name='d1')
    domain1 = DistrictDomain.objects.create(domain='school.org', district=d1)

    assert list(d1.email_domains)[0] == domain1

    d1.remove_email_domain("school.org")
    assert list(d1.email_domains) == []

def test_remove_domain_other_school(db):
    d1: District = District.objects.create(name='d1')
    d2: District = District.objects.create(name='d1')
    domain1 = DistrictDomain.objects.create(domain='blah.org', district=d1)
    domain2 = DistrictDomain.objects.create(domain='school.org', district=d2)

    d1.remove_email_domain("school.org")
    assert list(d1.email_domains) == [domain1]
    assert list(d2.email_domains) == [domain2]