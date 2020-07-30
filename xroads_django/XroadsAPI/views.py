from django.shortcuts import render
from rest_framework import generics

from rest_framework.generics import get_object_or_404
from XroadsAPI.serializers import *

# Create your views here.
def csrf(request):
    return render(request, template_name='home.html')


class GetClub(generics.RetrieveAPIView):
    model = Club
    serializer_class = ClubDetailSerializer

    def get_object(self):
        return get_object_or_404(Club, id=self.kwargs['club'])

class GetSchoolList(generics.ListAPIView):
    model = School
    serializer_class = BasicInfoSchoolSerial
    queryset = School.objects.all()

class GetClubOverview(generics.ListAPIView):
    model = Club
    serializer_class = BasicClubInfoSerial

    def get_queryset(self):
        return get_object_or_404(Club, school__in=self.kwargs['school'])


