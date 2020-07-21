from XroadsAPI.models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'is_anon', 'phone']
        allow_null=True

class MeetingDaysSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['day']

class AnonProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'is_anon', 'phone']
        allow_null=True

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Removes all anonymous users information from serialization
        for i, member in enumerate(rep['members']):
            if member['is_anon']:
                rep['members'][i] = {'is_anon': True}

        return rep

class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'
        allow_null = True

class BasicClubInfoSerial(serializers.ModelSerializer):
    meeting_days = MeetingDaysSerializer(many=True)

    class Meta:
        model = Club
        fields = ['id', 'description', 'main_img', 'is_visible', 'meeting_days']

class ClubAllInfoSerializer(serializers.ModelSerializer):
    meeting_days = MeetingDaysSerializer(many=True)
    members = AnonProfileSerializer(many=True)
    slides = SlideSerializer(many=True)

    class Meta:
        model = Club
        fields = '__all__'

class BasicInfoSchoolSerial(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['name', 'img']


