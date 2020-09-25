from XroadsAPI.models import *
from rest_framework.fields import empty

from XroadsAPI.models import *
import XroadsAuth.permisson_constants as PermConst
from XroadsAuth.permissions import Permissions

import XroadsAuth.models as AuthModels
from rest_framework import serializers

def email_exists(email):
    try:
        AuthModels.Profile.objects.get(email=email)
    except AuthModels.Profile.DoesNotExist:
        raise serializers.ValidationError('A user with that email does not exist')
    
    return email

class EmailListForm(serializers.Serializer):
    emails = serializers.ListField(child=serializers.EmailField())

    def __init__(self, data=empty, **kwargs):
        super().__init__(instance=None, data=data, **kwargs)

    @property
    def profiles(self):
        assert self.is_valid(), 'You cannot access emails if the values are not valid'
        profiles = []
        non_existant_emails = []

        for email in self.validated_data['emails']:
            try:
                profiles.append(AuthModels.Profile.objects.get(email=email))
            except AuthModels.Profile.DoesNotExist:
                non_existant_emails.append(email)
        
        return profiles, non_existant_emails
            
class AddAdminForm(serializers.Serializer):
    permissions = serializers.ListField(child=serializers.CharField())
    email = serializers.EmailField()

    # TODO make something that creates a "reserved account" if they put in an email that doesn't exist        

    def __init__(self, hier_role, data=empty, **kwargs):
        self.hier_role = hier_role
        super(serializers.Serializer, self).__init__(data=data, **kwargs)

    def validate_permissions(self, value):
        hier = PermConst.Hierarchy.get_hierarchy(self.hier_role)
        try:
            perm_class = Permissions(value, hier)
            return value
        except AssertionError:
            raise serializers.ValidationError(detail=f'Invalid permissions were attempted to be assign for {self.hier_role} role')

class RemoveAdminForm(serializers.Serializer):
    email = serializers.EmailField(validators=[email_exists])

    # TODO make sure you remove from permissions if reserved user
    

class CreateClubForm(EmailListForm, serializers.ModelSerializer):
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
