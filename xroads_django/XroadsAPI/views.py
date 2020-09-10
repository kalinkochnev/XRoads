from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from XroadsAPI.serializers import *


# Create your views here.
def csrf(request):
    return render(request, template_name='home.html')


# TODO change querysets
class DistrictViewset(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]

class SchoolViewset(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = BasicInfoSchoolSerial
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        school_id = self.kwargs['school_pk']
        queryset = Club.objects.filter(school=school_id)
        return Response(BasicClubInfoSerial(queryset, many=True).data)

    @action(detail=True, methods=['post'])
    def join_club(self, request):
        pass

    @action(detail=True, methods=['post'])
    def leave_club(self, request):
        pass
