from rest_framework import serializers
from rest_framework.generics import mixins
from XroadsAPI.models import *

class BasicClubInfoSerial(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'img', 'is_visible']


class BasicInfoSchoolSerial(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'img']


class DistrictSerializer(serializers.ModelSerializer):
    schools = BasicInfoSchoolSerial(many=True)

    class Meta:
        model = District
        fields = '__all__'


class ClubDetailSerializer(serializers.ModelSerializer):
    slides = serializers.ListField(child=serializers.URLField())

    class Meta:
        model = Club
        exclude = ['code', 'hidden_info']

class SchoolDetailSerializer(serializers.ModelSerializer):
    clubs = BasicClubInfoSerial(many=True)

    class Meta:
        fields = '__all__'
        model = School


class ClubEditSerializer(serializers.ModelSerializer):
    slides = serializers.ListField(child=serializers.URLField(), read_only=True)

    class Meta:
        model = Club
        fields = '__all__'
        read_only_fields = ['img', 'name']


