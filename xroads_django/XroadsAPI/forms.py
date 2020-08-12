from XroadsAuth.models import Profile
from XroadsAPI.models import *
from rest_framework import serializers
from XroadsAPI.permissions import Hierarchy, Permissions
from XroadsAPI.serializers import EmailSerializer, PermissionSerializer
from rest_framework.fields import empty


class UserEmailForm(serializers.Serializer):
    profile_emails = EmailSerializer(many=True)

    def __init__(self, hier_role, instance=None, data=empty, **kwargs):
        self.hier_role = hier_role
        super().__init__(instance=instance, data=data, **kwargs)

    
    @property
    def profiles(self):
        assert self.is_valid(), 'You cannot access emails if the values are not valid'
        return [Profile.objects.get(email=email) for email in self.profile_emails]

    def validate_profile_emails(self, values):
        invalid_emails = []
        for email in values:
            if not Profile.objects.filter(email=email).exists():
                invalid_emails.append(email)
        
        if len(invalid_emails) != 0:
            raise serializers.ValidationError(detail=f'Invalid emails given: {invalid_emails}')

        return values

class AdminRoleForm(UserEmailForm):
    permissions = PermissionSerializer(many=True)

    def validate_permissions(self, values):
        hier = Hierarchy.get_hierarchy(self.hier_role)
        perm_class = Permissions([], hier)
        if not perm_class.is_allowed(values):
            raise serializers.ValidationError(detail=f'Invalid permissions were attempted to be assign for {self.hier_role} role')

        return values

class CreateClubForm(UserEmailForm, serializers.ModelSerializer):
    class Meta:
        fields = ['name']
        model = Club

    def create(self, validated_data):
        club = Club(
            name=validated_data['name'],
            description='',
            hours='',
            is_visible=False,
        )
        club.add_admin(*self.profiles, perms=['__all__'])
        club.save()
