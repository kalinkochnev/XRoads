from rest_framework import serializers
from utils.serializers import DynamicModelSerializer
from rest_framework.generics import mixins
from api.models import *



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['club']

    def create(self, validated_data):
        validated_data['club'] = self.context['club']
        return super().create(validated_data)



    def validate(self, data):
        if data.get('start') > data.get('end'):
            time_str = data['start'].strftime("%H:%M:%S")
            raise serializers.ValidationError(
                "Pick a time later than " + time_str)
       
        return data

class ClubAll(DynamicModelSerializer):
    slides = serializers.ListField(child=serializers.URLField())
    events = EventSerializer(many=True)
    
    class Meta:
        model = Club
        fields = '__all__'

ClubBasic = ClubAll.sub_serializer(fields=['id', 'contact', 'name', 'img', 'is_visible', 'slug'])

class SchoolAll(DynamicModelSerializer):
    clubs = ClubBasic(many=True)
    week_events = EventSerializer(many=True)

    class Meta:
        model = School
        fields = '__all__'


SchoolNoClubs = SchoolAll.sub_serializer(
    fields=['clubs', 'week_events'], exclude=True)


class DistrictAll(DynamicModelSerializer):
    schools = SchoolNoClubs(many=True)

    class Meta:
        model = District
        fields = ['id', 'name', 'schools']

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
