import pytest
from django.contrib.auth import get_user_model, authenticate
from XroadsAPI.models import *
from XroadsAuth.models import *
from django.core.exceptions import FieldError


@pytest.fixture
def setup_user():
    User = get_user_model()
    return User.objects.create_user(email='norm@user.com', password='testpassword')


def test_norm_user_creation(db, setup_user):
    User = get_user_model()
    user = setup_user
    assert user.email == 'norm@user.com'
    assert user.is_active == True
    assert user.is_staff == False
    assert user.is_superuser == False

    # test username attribute does not exist because it shouldn't
    assert user.username == None

    # test when certain parameters are missing it raises the errors
    with pytest.raises(TypeError):
        assert User.objects.create_user()
    with pytest.raises(TypeError):
        assert User.objects.create_user(
            username='testuser', password='testpassword')
    with pytest.raises(ValueError):
        assert User.objects.create_user(
            email='norm@user.com', username='testuser', password='')
    with pytest.raises(ValueError):
        assert User.objects.create_user(email='', username='', password='')


def test_email_address_added_dj_all_auth(db):
    

def test_create_superuser(db):
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        email='super@user.com', password='foo')
    assert admin_user.email == 'super@user.com'
    assert admin_user.is_active == True
    assert admin_user.is_staff == True
    assert admin_user.is_superuser == True

    # test username attribute does not exist
    assert admin_user.username == None

    # tests that if is_superuser=False that it raises an error
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email='super@user.com', password='foo', is_superuser=False
        )


def test_authentication(db):
    User = get_user_model()

    # check that auth returns a user object that is the expected one
    user_email = 'email@user.com'
    user_password = 'testpassword'
    user1 = User.objects.create_user(email=user_email, password=user_password)
    returned_user = authenticate(email=user_email, password=user_password)
    assert user1 == returned_user

    # check that None is returned if password is incorrect
    user_email = 'email@user.com'
    user_wrong_password = 'yikes'
    user2 = User.objects.create_user(
        email='email2@user.com', password='testpassword')
    returned_user = authenticate(
        email=user_email, password=user_wrong_password)

    assert returned_user == None


def test_signup(db):
    User = get_user_model()

    # should return a user object since it doesn't exist
    user_email = 'new@email.com'
    user_pass = 'somepass'
    new_user = User.objects.signup(user_email, user_pass)
    assert new_user.email == user_email
    assert new_user.check_password(user_pass) is True

    # should return none since user with that email already exists
    other_user = User.objects.signup(user_email, 'password')
    assert other_user is None


# Testing profile methods --------------------------------------------


@pytest.fixture
def sample_user():
    email = "kalin.kochnev@gmail.com"
    password = "2323hj23hk2h"
    first_name = "kalin"
    last_name = "kochnev"
    phone_number_str = '5188881542'
    is_anon = True
    return Profile(email=email, password=password, first_name=first_name, last_name=last_name, phone=phone_number_str, is_anon=True)


@pytest.mark.parametrize("input_phone,expected", [
    ['518-888-1542', "5188881542"],
    ['(518) 888-1542', "5188881542"],
    ['518 888 1542', "5188881542"],
    ['5 1 8 8 8 8 1 5 4 2', "5188881542"]
])
def test_parse_phone_valid_len(input_phone, expected):
    assert Profile.parse_phone(input_phone) == expected


@pytest.mark.parametrize('input_phone', ['518-888-154211111', '123-4567', '12345678'])
def test_parse_phone_invalid_len(input_phone):
    with pytest.raises(FieldError) as context:
        assert Profile.parse_phone(input_phone)


def test_creation_optional(db, sample_user):
    prof: Profile = Profile.create_profile(
        email=sample_user.email, password=sample_user.password, first=sample_user.first_name, last=sample_user.last_name)
    assert prof.phone_num is None
    assert prof.is_anon is False

    assert prof.first_name == sample_user.first_name
    assert prof.last_name == sample_user.last_name
    assert prof.email == sample_user.email

    # test second object is created normally (Added due to bug where you can't only use email and password for User model creation)
    prof2 = Profile.create_profile(
        email="something@gmail.com", password="a", first="b", last="c")


def test_creation_all_params(db, sample_user):
    prof: Profile = Profile.create_profile(email=sample_user.email, password=sample_user.password,
                                           first=sample_user.first_name, last=sample_user.last_name, phone=sample_user.phone, is_anon=sample_user.is_anon)
    assert prof.phone_num == sample_user.phone_num
    assert prof.is_anon == sample_user.is_anon


def test_create_test_prof(create_test_prof):
    # Test that valid attributes are set
    prof_num = 1
    prof = create_test_prof(prof_num)
    assert prof.email == f'test{prof_num}@email.com'
    assert len(prof.phone) == 10
    assert prof.first_name == f'testfirst{prof_num}'
    assert prof.last_name == f'testlast{prof_num}'

    # Test that you can override params
    prof_num = 2
    test_email = 'hello@gmail.com'
    prof2 = create_test_prof(prof_num, email=test_email)
    assert prof2.email == test_email
