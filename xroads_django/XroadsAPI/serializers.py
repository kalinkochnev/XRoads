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
        read_only_fields = ['club', 'views']

    def validate(self, data):
        if data['start'] > data['end']:
            time_str = data['start'].strftime("%H:%M:%S")
            raise serializers.ValidationError(
                "Pick a time later than " + time_str)
        return data

    def create(self, validated_data):
        event = super(EventSerializer, self).create(
            {**validated_data, 'club': self.context['club']})
        return event


class ClubDetailSerializer(serializers.ModelSerializer):
    slides = serializers.ListField(child=serializers.URLField())
    events = EventSerializer(many=True)

    class Meta:
        model = Club
        exclude = ['code', 'extra_info']


class SchoolDetailSerializer(serializers.ModelSerializer):
    clubs = BasicClubInfoSerial(many=True)
    curr_featured_order = serializers.IntegerField()
    week_events = EventSerializer(many=True)

    class Meta:
        exclude = ['featured']
        model = School


class ClubEditSerializer(serializers.ModelSerializer):
    slides = serializers.ListField(
        child=serializers.URLField(), read_only=True)
    school = BasicInfoSchoolSerial(read_only=True)
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = '__all__'
        read_only_fields = ['img', 'name']
