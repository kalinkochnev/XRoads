from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

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

    @action(detail=True, methods=['get'])
    def club_code(self, request, *args, **kwargs):
        try:
            club = Club.objects.get(school=self.get_object(), code=request.query_params['code'])
            return Response(BasicClubInfoSerial(club).data, status=status.HTTP_200_OK)
        except Club.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ClubViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubDetailSerializer

    def list(self, request, *args, **kwargs):
        school_id = self.kwargs['school_pk']
        queryset = Club.objects.filter(school=school_id)
        return Response(BasicClubInfoSerial(queryset, many=True).data)
