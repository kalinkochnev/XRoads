import tempfile
from collections import OrderedDict

import pytest

from XroadsAPI.serializers import *
from XroadsAPI.slide import SlideTemplates
from XroadsAuth.models import Profile

def test_slide_serialization(db, temp_img, create_club):
    # Creates temp test iamge
    temp_file = tempfile.NamedTemporaryFile()
    test_image = temp_img(temp_file)

    video_url = "youtube.com/do-stuff"
    position = 1
    img = test_image.name

    # Set class variable to prevent conflicts
    temp_id = 1
    template_args = ['img', 'video_url']
    template = SlideTemplates.Template(
        temp_id=temp_id, name="test", required=template_args)
    SlideTemplates.templates = [template]
    club = create_club()

    # Chooses from test values based on template_args
    slide = SlideTemplates.new_slide(
        temp_id, club=club, position=position, img=img, video_url=video_url)

    expected = {
        'id': slide.id,
        'template_type': temp_id,
        'position': position,
        'video_url': video_url,
        'img': slide.img.url,
        'text': None,
        'club': club.id,
    }

    assert SlideSerializer(slide).data == expected


def test_club_creation(db, temp_img):
    # Creates temp test iamge
    temp_file = tempfile.NamedTemporaryFile()
    test_image = temp_img(temp_file)

    club: Club = Club.objects.create(
        name="a", description="b", main_img=test_image.name, hours="7hrs/week", is_visible=True, join_promo="Join today")
    data = OrderedDict({
        'name': club.name,
        'description': club.description,
        'main_img': club.main_img.url,
        'hours': club.hours,
        'is_visible': club.is_visible,
        'members': [],
        'slides': [],
        'join_promo': club.join_promo,
    })

    serializer = ClubDetailSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)
