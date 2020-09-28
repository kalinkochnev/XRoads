from rest_framework import serializers

from XroadsAPI.models import *
import XroadsAuth.models as AuthModels
import XroadsAuth.serializers as AuthSerializers
from django.shortcuts import get_object_or_404


class SlideListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        slides = []
        for i, data in enumerate(validated_data):
            data['position'] = i
            data['club'] = Club.objects.get(id=self.context['club'])
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


class ClubDetailSerializer(serializers.ModelSerializer):
    members = AuthSerializers.AnonProfileSerializer(
        many=True, fields=('first_name', 'last_name'))
    slides = SlideSerializer(many=True)

    class Meta:
        model = Club
        fields = '__all__'


class BasicInfoSchoolSerial(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'img']


class DistrictSerializer(serializers.ModelSerializer):
    schools = BasicInfoSchoolSerial(many=True)

    class Meta:
        model = District
        fields = '__all__'

# ADMIN SERIALIZERS ---------------------


class ClubEditorSerializer(serializers.ModelSerializer):
    members = AuthSerializers.ProfileSerializer(many=True, read_only=True)
    slides = SlideSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = '__all__'
        read_only_fields = ['main_img']


class SchoolAdminSerializer(serializers.ModelSerializer):
    clubs = BasicClubInfoSerial(many=True)
    students = AuthSerializers.ProfileSerializer(many=True)

    class Meta:
        model = School
        fields = '__all__'


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField()

    def create(self, validated_data):
        request = self.context.get('request')
        club = self.context.get('club')
        return Question.objects.create(asker=request.user, club=club, question=validated_data.get('question'))


class GetQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['question', 'answer', 'id']
        model = Question


class AnswerQuestionSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all())
    answer = serializers.CharField()

    def create(self, validated_data):
        question = validated_data.get('question')
        question.answer = validated_data.get('answer')
        question.save()
        return question
