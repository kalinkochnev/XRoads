from django.test import TestCase
from XroadsAPI.models import Profile
from XroadsAPI.serializers import ProfileSerializer, AnonProfileSerializer
from XroadsAPI.tests.test_models import TestProfileModel
class TestProfileSerializer(TestCase):
    def test_serialization(self):
        user_obj:Profile = Profile.objects.create_user(email="a@email.com", password="password", first_name="a", last_name="b", phone="1234567899", is_anon=True)
        expected = {
            'id': user_obj.id,
            'email': user_obj.email,
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name,
            'is_anon': user_obj.is_anon,
            'phone_num': user_obj.phone_num,
        }

        assert expected == ProfileSerializer(user_obj).data

    def test_optional_fields(self):
        user_obj = Profile.objects.create_user(email="a@email.com", password="password", first_name="a", last_name="b")
        expected = {
            'id': user_obj.id,
            'email': user_obj.email,
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name,
            'is_anon': user_obj.is_anon,
            'phone_num': None
        }

        assert expected == ProfileSerializer(user_obj).data

class TestAnonProfileSerializer(TestCase):
    def generate_test_profiles(self, num):
        visible = []
        invisible = []
        for i in range(num):
            if i % 2 == 0:
                visible.append(TestProfileModel.create_test_prof(num))
            else:
                invisible.append(TestProfileModel.create_test_prof(num))
        return visible, invisible

    def test_remove_anon_profiles(self):
        prof1 = TestProfileModel.create_test_prof(1, is_anon=True)
        expected = {
            'is_anon': True
        }

        assert AnonProfileSerializer(prof1).data == expected
    
    def test_not_anon_serialization(self):
        prof1 = TestProfileModel.create_test_prof(1)
        expected = {
            'id': prof1.id,
            'email': prof1.email,
            'first_name': prof1.first_name,
            'last_name': prof1.last_name,
            'is_anon': prof1.is_anon,
            'phone_num': prof1.phone_num,
        }

        assert AnonProfileSerializer(prof1).data == expected
        