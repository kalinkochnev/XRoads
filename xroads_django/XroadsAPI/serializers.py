from rest_framework import serializers
from rest_framework.generics import mixins
from XroadsAPI.models import *


class BasicClubInfoSerial(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = ['id', 'name', 'description',
                  'img', 'is_visible', 'featured_order']


class BasicInfoSchoolSerial(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'img', 'club_contact']


class DistrictSerializer(serializers.ModelSerializer):
    schools = BasicInfoSchoolSerial(many=True)

    class Meta:
        model = District
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ClubDetailSerializer(serializers.ModelSerializer):
    slides = serializers.ListField(child=serializers.URLField())
    events = EventSerializer(many=True)

    class Meta:
        model = Club
        exclude = ['code', 'extra_info']


class SchoolDetailSerializer(serializers.ModelSerializer):
    clubs = BasicClubInfoSerial(many=True)
    curr_featured_order = serializers.IntegerField()

    class Meta:
        exclude = ['featured']
        model = School


class ClubEditSerializer(serializers.ModelSerializer):
    slides = serializers.ListField(
        child=serializers.URLField(), read_only=True)
    school = BasicInfoSchoolSerial(read_only=True)
    events = EventSerializer(many=True)

    class Meta:
        model = Club
        fields = '__all__'
        read_only_fields = ['img', 'name']


