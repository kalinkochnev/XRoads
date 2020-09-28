from testutils.conftest import temp_img
from django.core.files.uploadedfile import SimpleUploadedFile

from XroadsAPI.tests.test_model_club import club_fix
import tempfile
from collections import OrderedDict
import random
import pytest

from XroadsAPI.serializers import *
from XroadsAPI.slide import SlideTemplates
from XroadsAuth.models import Profile

def test_slide_serialization(db, temp_img, create_club, ):
    # Creates temp test iamge
    temp_file = tempfile.NamedTemporaryFile()
    test_image = temp_img(temp_file)

    video_url = "youtube.com/do-stuff"
    position = 1
    img = test_image.name
    body = "body text"

    # Set class variable to prevent conflicts
    temp_id = 1
    template_args = ['img', 'video_url']
    template = SlideTemplates.Template(
        temp_id=temp_id, name="test", disabled=[])
    SlideTemplates.templates = [template]
    club = create_club()

    # Chooses from test values based on template_args
    slide = SlideTemplates.new_slide(
        temp_id, club=club, position=position, img=img, video_url=video_url, body=body)

    expected = {
        'template_type': temp_id,
        'position': position,
        'video_url': video_url,
        'img': slide.img.url,
        'text': None,
        'club': club.id,
        'body': body,
    }

    assert SlideSerializer(slide).data == expected

def test_slide_position_computed(create_test_slide, create_club, temp_img):
    club = create_club()
    slides = []

    for i in range(4):
        template, params = create_test_slide()
        slide = club.add_slide(template.temp_id, **params)

        slide.video_url = "https://www.youtube.comW"
        slide.save()
        slides.append(slide)

    # shuffle list positions
    random.shuffle(slides)

    input_slide_data = SlideSerializer(slides, many=True).data
    for item in input_slide_data:
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        test_image = temp_img(temp_file)

        item['img'] = SimpleUploadedFile(name=test_image.name, content=open(test_image.name, 'rb').read(), content_type='image/jpeg')

    loaded_slides = SlideListSerializer(child=SlideSerializer(), context={'club': club})
    
    loaded_slides = loaded_slides.create(input_slide_data)

    for i, slide in enumerate(loaded_slides):
        assert slide.position == i
    

    
    



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
