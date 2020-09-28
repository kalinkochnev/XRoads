import tempfile

import pytest

from XroadsAuth.models import Profile, RoleModel
from XroadsAPI.models import School, District, Club
from XroadsAuth.permissions import Role


@pytest.fixture
def club_fix(db, temp_img):
    profile = Profile.create_profile(
        email="a@gmail.com", password="password", first="kalin", last="kochnev")
    name = "Test Club"
    description = "This is a club description"
    commitment = "7hrs/week"
    is_visible = False
    join_promo = "Join our club"

    temp_file = tempfile.NamedTemporaryFile()
    test_image = temp_img(temp_file)
    return Club.objects.create(name=name, description=description, main_img=test_image.name, hours=commitment, is_visible=is_visible, join_promo = join_promo)


def test_add_slide(club_fix, create_test_slide):
    template, params = create_test_slide()
    slide1 = club_fix.add_slide(template.temp_id, **params)
    slide2 = club_fix.add_slide(template.temp_id, **params)

    assert club_fix.slides.count() == 2
    assert slide1.position == 1
    assert slide2.position == 2


def test_remove_slide(club_fix, create_test_slide):
    template, params = create_test_slide()
    slide1 = club_fix.add_slide(template.temp_id, **params)

    club_fix.remove_slide(1)
    assert club_fix.slides.count() == 0


def test_join(club_fix, create_test_prof):
    profile = create_test_prof(1)
    club_fix.join(profile)
    assert club_fix.members.count() == 1


def test_leave(club_fix, create_test_prof):
    profile = create_test_prof(1)
    club_fix.join(profile)
    club_fix.leave(profile)

    assert club_fix.members.count() == 0


def test_add_club(db, create_club):
    club = create_club()
    school = School.objects.create(name="Some School")
    school.add_club(club)

    assert school.clubs.count() == 1

def test_get_editors(db, role_model_instances, create_test_prof, perm_const_override):
    d1, s1, c1 = role_model_instances()
    profiles = [create_test_prof(i) for i in range(3)]

    role = Role.from_start_model(c1)
    role.permissions.add('hide-club')

    for prof in profiles:
        role.give_role(prof)

    # Tests what happens if there are multiple RoleModel instances with the same role_name
    role2 = Role.from_start_model(c1)
    role2.permissions.add('add-admin')
    profiles.append(create_test_prof(4))
    role2.give_role(profiles[-1])

    for prof in profiles:
        assert prof in list(c1.editors) 