from django.http import request
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from XroadsAPI.serializers import *


class DistrictViewset(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class SchoolViewset(viewsets.ReadOnlyModelViewSet, GenericViewSet):
    queryset = School.objects.all()
    serializer_class = BasicInfoSchoolSerial

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SchoolDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def club_code(self, request, *args, **kwargs):
        try:
            club = Club.objects.get(
                school=self.get_object(), code=request.query_params['code'])
            return Response(BasicClubInfoSerial(club).data, status=status.HTTP_200_OK)
        except (Club.DoesNotExist, KeyError):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['get'])
    def event_info(self, request, *args, **kwargs):
        event_id = self.request.query_params.get('')
        email = self.request.query_params.get('email', None)

        if email is not None and event_id is not None:
            district = District.match_district(email)

            try:
                Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                

            club: Club = self.get_object()
            if district == club.district:
                club.send_extra_info(email)
                return Response({}, status=status.HTTP_200_OK)
        return Response({'message': 'The email provided was invalid or is not allowed to access'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ClubViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubDetailSerializer

    @action(detail=True, methods=['get'])
    def club_info(self, request, *args, **kwargs):
        email = self.request.query_params.get('email', None)
        if email is not None:
            district = District.match_district(email)

            club: Club = self.get_object()
            if district == club.district:
                club.send_extra_info(email)
                return Response({}, status=status.HTTP_200_OK)
        return Response({'message': 'The email provided was invalid or is not allowed to access'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request, *args, **kwargs):
        school_id = self.kwargs['school_pk']
        queryset = Club.objects.filter(school=school_id)
        return Response(BasicClubInfoSerial(queryset, many=True).data)

class EventViewset(viewsets.ReadOnlyModelViewSet):
    class Meta:
        model = 