from rest_framework import serializers

from XroadsAPI.models import *
import XroadsAuth.models as AuthModels


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthModels.Profile
        fields = ['id', 'email', 'first_name', 'last_name', 'is_anon']
        allow_null = True

class AnonProfileSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AuthModels.Profile
        fields = ['id', 'email', 'first_name', 'last_name', 'is_anon']
        allow_null = True

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Removes all anonymous users information from serialization
        if 'is_anon' in rep and rep['is_anon']:
            return {'is_anon': True}
        return rep


class SlideSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'
        allow_null = True

class BasicClubInfoSerial(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'main_img', 'is_visible']

class ClubDetailSerializer(serializers.ModelSerializer):
    members = AnonProfileSerializer(many=True, fields=('first_name', 'last_name'))
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
    members = ProfileSerializer(many=True)
    slides = SlideSerializer(many=True)
    class Meta:
        model = Club
        fields = '__all__'

class SchoolAdminSerializer(serializers.ModelSerializer):
    clubs = BasicClubInfoSerial(many=True)
    students = ProfileSerializer(many=True)

    class Meta:
        model = School
        fields = '__all__'


    