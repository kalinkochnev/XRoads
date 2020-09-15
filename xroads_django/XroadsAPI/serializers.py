from rest_framework import serializers

from XroadsAPI.models import *
import XroadsAuth.models as AuthModels
import XroadsAuth.serializers as AuthSerializers


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'
        allow_null = True

class BasicClubInfoSerial(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'main_img', 'is_visible']

class ClubDetailSerializer(serializers.ModelSerializer):
    members = AuthSerializers.AnonProfileSerializer(many=True, fields=('first_name', 'last_name'))
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
    members = AuthSerializers.ProfileSerializer(many=True)
    slides = SlideSerializer(many=True)
    class Meta:
        model = Club
        fields = '__all__'

class SchoolAdminSerializer(serializers.ModelSerializer):
    clubs = BasicClubInfoSerial(many=True)
    students = AuthSerializers.ProfileSerializer(many=True)

    class Meta:
        model = School
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    asker = AuthSerializers.AnonProfileSerializer(read_only=True)
    club = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        club = self.context.get('club')
        return Question.objects.create(asker=request.user, club=club, question=validated_data.get('question'), answer=validated_data.get('answer'))