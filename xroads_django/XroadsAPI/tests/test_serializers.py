from django.test import TestCase
from XroadsAPI.models import Profile
from XroadsAPI.serializers import UserSerializer
from XroadsAPI.tests.test_models import TestProfileModel
class TestUserSerializer(TestCase):
    def test_serialization(self):
        user_obj = Profile.objects.create_user(email="a@email.com", password="password", first_name="a", last_name="b")
        expected = {
            'id': user_obj.id,
            'email': user_obj.email,
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name
        }

        assert expected == UserSerializer(user_obj).data


class TestProfileSerializer(TestCase):
    def test_blank_fields_allowed(self):
        pass