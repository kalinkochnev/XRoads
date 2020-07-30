from XroadsAPI.models import *
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from XroadsAPI.serializers import *

class ProfileAdmin(generics.UpdateAPIView):
    model = Profile
    serializer_class = ProfileAdminSerializer

    def get_object(self):
        return get_object_or_404(Profile, id=self.kwargs['pk'])

class ClubEditor(generics.RetrieveUpdateAPIView):
    model = Club
    serializer_class = ClubEditorSerializer

    def get_object(self):
        return get_object_or_404(Club, id=self.kwargs['club'])

class SchoolAdmin(generics.RetrieveUpdateAPIView):
    model = School
    serializer_class = School

    def get_object(self):
        return get_object_or_404(School, id=self.kwargs['school'])

class DistrictAdmin(generics.RetrieveUpdateAPIView):
    model = District
    serializer_class = DistrictAdmin

    def get_object(self):
        return get_object_or_404(District, id=self.kwargs['district'])

class CreateClub(generics.CreateAPIView):
    model = Club
    serializer_class = ClubDetailSerializer
