import tempfile

import pytest

from XroadsAPI.models import *
from XroadsAPI.slide import SlideTemplates


def test_disabled_args():
    template = SlideTemplates.Template(
        temp_id=1, name="img", disabled=['video_url', 'body'])

    invalid_arg = ['hello']
    assert template.has_proper_args(invalid_arg) is False

    # Position not included
    poss_arg = ['img']
    assert template.has_proper_args(poss_arg) is False

    poss_arg = ['img', 'position']
    assert template.has_proper_args(poss_arg) is True


def test_get_template(template_setup):
    temp_id = template_setup.temp_id
    assert SlideTemplates.get(temp_id) == template_setup


def test_template_create_slide(db, temp_img, template_setup, create_club):
    # This creates a temporary image file to use
    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    test_image = temp_img(temp_file)

    slide_text = "this is a test"
    video_url = 'youtube.com/testing-video'
    args = [video_url, slide_text, test_image.name]
    useable_args = ['video_url', 'text', 'img']

    template_kwargs = dict(zip(useable_args, args))
    club = create_club()
    slide = SlideTemplates.new_slide(
        template_setup.temp_id, club=club, position=1, **template_kwargs)

    assert slide.img is not None
    assert slide.text == slide_text
    assert slide.video_url == video_url


def test_less_args():
    template = SlideTemplates.Template(temp_id=1, name="img", disabled=['video_url', 'body'])


def test_create_invalid_slide(template_setup, create_club):
    club = create_club()
    with pytest.raises(SlideParamError) as e:
        assert SlideTemplates.new_slide(
            template_setup.temp_id, body="stuff", club=club, position=1)


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
