import tempfile

import pytest

from XroadsAPI.models import *
from XroadsAPI.slide import SlideTemplates


def test_template_match_args_valid(template_setup):
    test_args = ['text', 'video_url', 'img', 'position']
    assert template_setup.args_match(test_args) is True


def test_template_position_arg_required(template_setup):
    test_args = ['text', 'video_url', 'img']
    assert template_setup.args_match(test_args) is False


def test_template_match_args_invalid(template_setup):
    test_args = ['text']
    assert template_setup.args_match(test_args) is False


def test_get_template(template_setup):
    temp_id = template_setup.temp_id
    assert SlideTemplates.get(temp_id) == template_setup


def test_template_create_slide(db, temp_img, template_setup, create_club):
    # This creates a temporary image file to use 
    #  testing!!! The decorator overrides the django settings
    temp_file = tempfile.NamedTemporaryFile()
    test_image = temp_img(temp_file)

    slide_text = "this is a test"
    video_url = 'youtube.com/testing-video'
    args = [video_url, slide_text, test_image.name]

    template_kwargs = dict(zip(template_setup.required_args, args))
    club = create_club()
    slide = SlideTemplates.new_slide(template_setup.temp_id, club=club, position=1, **template_kwargs)

    assert slide.img is not None
    assert slide.img == test_image
    assert slide.text == slide_text
    assert slide.video_url == video_url


def test_create_invalid_slide(template_setup, create_club):
    club = create_club()
    with pytest.raises(SlideParamError) as e:
        assert SlideTemplates.new_slide(template_setup.temp_id, club=club, position=1)

def test_slide_ordered_by_pos(create_test_slide, role_model_instances):
    d1, s1, c1 = role_model_instances()
    slides_data = [create_test_slide() for i in range(3)]
    slides = []
    for template, args in slides_data:
        slide = c1.add_slide(template.temp_id, **args, save=False)
        slides.append(slide)
    c1.make_save(True)

    club_slides = c1.slides
    assert club_slides[0] == slides[0]
    assert club_slides[1] == slides[1]
    assert club_slides[2] == slides[2]



def test_set_club_slides():
    # Test positions are adjusted based on array order
    # Test slides are set to the club
    pass