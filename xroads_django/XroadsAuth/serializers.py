from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from XroadsAPI.models import District, Club
from XroadsAuth.models import HierarchyPerms, Profile
from XroadsAuth.utils import DynamicFieldsModelSerializer

class ProfileSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(child=serializers.CharField(), read_only=True, source='simple_perm_strs')
    joined_clubs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'email', 'first_name', 'last_name', 'is_anon', 'permissions', 'school', 'district', 'joined_clubs']
        allow_null = True

class AnonProfileSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'first_name', 'last_name', 'is_anon']
        allow_null = True

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Removes all anonymous users information from serialization
        if 'is_anon' in rep and rep['is_anon']:
            return {'is_anon': True}
        return rep


class CustomRegister(RegisterSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    def custom_signup(self, request, user):
        pass

    def validate(self, data):
        is_valid = super().validate(data)

        if District.match_district(data['email']) is None:
            raise serializers.ValidationError('Your district doesn\'t use xroads :(  Ask them to contact us!')
        
        return is_valid

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }




class CustomLoginSerializer(LoginSerializer):
    pass

    