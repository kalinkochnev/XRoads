from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework import viewsets
from XroadsAPI.serializers import *
from rest_framework.response import Response

# Create your views here.
def csrf(request):
    return render(request, template_name='home.html')

class UserViewset(viewsets.GenericViewSet, generics.RetrieveAPIView):
    serializer_class = AnonProfileSerializer
    queryset = Profile

# TODO change querysets
class DistrictViewset(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class SchoolViewset(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = BasicInfoSchoolSerial

    # TODO make permission that checks the request user belongs to the object
    @action(detail=True, methods=['post'])
    def join_school(self, request):
        pass

    @action(detail=True, methods=['post'])
    def leave_school(self, request):
        pass


class ClubViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.all()
    # TODO change the serializer depending on what request it is
    serializer_class = ClubDetailSerializer

    @action(detail=True, methods=['post'])
    def join_club(self, request):
        pass

    @action(detail=True, methods=['post'])
    def leave_club(self, request):
        pass
