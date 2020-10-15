from rest_framework import serializers
from XroadsAPI.models import *
from django.shortcuts import get_object_or_404

class BasicClubInfoSerial(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'main_img', 'is_visible']


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
    slides = SlideSerializer(many=True) # TODO change this to return google slide ids

    class Meta:
        model = Club
        fields = '__all__'
