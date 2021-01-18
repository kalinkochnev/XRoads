from rest_framework import serializers
from utils.serializers import DynamicModelSerializer
from rest_framework.generics import mixins
from api.models import *


class ClubAll(DynamicModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


ClubBasic = ClubAll.to_serializer(fields=['name', 'img', 'is_visible', 'slug'])


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


class SchoolAll(DynamicModelSerializer):
    clubs = ClubBasic(many=True)
    week_events = EventSerializer(many=True)

    class Meta:
        model = School
        fields = '__all__'


SchoolNoClubs = SchoolAll.to_serializer(
    fields=['clubs', 'week_events'], exclude=True)


class DistrictAll(DynamicModelSerializer):
    schools = SchoolNoClubs(many=True)

    class Meta:
        model = District
        fields = '__all__'

    def create(self, validated_data):
        event = super(EventSerializer, self).create(
            {**validated_data, 'club': self.context['club']})
        return event


class ClubEditSerializer(serializers.ModelSerializer):
    slides = serializers.ListField(
        child=serializers.URLField(), read_only=True)
    school = SchoolNoClubs(read_only=True)
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = '__all__'
        read_only_fields = ['img', 'name']
