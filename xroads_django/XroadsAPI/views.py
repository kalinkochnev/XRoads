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
    lookup_field = 'pk'
    queryset = Profile
# TODO change querysets
class DistrictViewset(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class SchoolViewset(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = BasicInfoSchoolSerial

    @action(detail=True, methods=['post'], )
    def join_school(self, request):
        pass


class ClubViewset(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClubDetailSerializer
        elif self.action == 'list':
            return BasicClubInfoSerial
    # TODO 
    def get_queryset(self):
        school = self.kwargs['']
