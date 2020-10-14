from rest_framework import serializers
from XroadsAPI.models import *
from django.shortcuts import get_object_or_404


class SlideListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        slides = []
        for i, data in enumerate(validated_data):
            data['position'] = i
            data['club'] = self.context['club']
            slides.append(self.child.create(data))
        return slides


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        exclude = ['id']
        allow_null = True
        list_serializer_class = SlideListSerializer


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
    slides = SlideSerializer(many=True)

    class Meta:
        model = Club
        fields = '__all__'
