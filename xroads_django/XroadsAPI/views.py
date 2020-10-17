from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from XroadsAPI.serializers import *


class DistrictViewset(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class SchoolViewset(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = BasicInfoSchoolSerial

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SchoolDetailSerializer(instance)
        return Response(serializer.data)


class ClubViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubDetailSerializer

    def list(self, request, *args, **kwargs):
        school_id = self.kwargs['school_pk']
        queryset = Club.objects.filter(school=school_id)
        return Response(BasicClubInfoSerial(queryset, many=True).data)
