from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from XroadsAPI.models import District
from XroadsAuth.models import HierarchyPerms


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

# This should be used for read only
class PermissionSerializer(serializers.Serializer): 
    clubs = serializers.ID