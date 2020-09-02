from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck
from dj_rest_auth.jwt_auth import JWTCookieAuthentication

class CustomRegister(RegisterSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }


