from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
import api.serializers as serializers
from api.models import *

def csrf(request):
    return render(request, template_name='backend/templates/csrf.html')

# Create your views here.
class DistrictViewset(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = serializers.DistrictAll


# class SchoolViewset(viewsets.ReadOnlyModelViewSet):
#     queryset = School.objects.all()
#     serializer_class = serializers.SchoolAll
#     lookup_field = 'slug'


class ClubViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.all()
    serializer_class = serializers.ClubBasic
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.ClubAll(instance)
        return Response(serializer.data)

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
        school_slug = self.kwargs['school_slug']
        queryset = Club.objects.filter(school__slug=school_slug)
        return Response(serializers.ClubAll(queryset, many=True).data)

class SchoolViewset(viewsets.ReadOnlyModelViewSet, viewsets.GenericViewSet):
    queryset = School.objects.all()
    serializer_class = serializers.SchoolAll
    lookup_field = "slug"


    @action(detail=True, methods=['get'])
    def club_code(self, request, *args, **kwargs):
        try:
            club = Club.objects.get(
                school=self.get_object(), code=request.query_params['code'])
            data = serializers.ClubBasic(club).data
            return Response(data, status=status.HTTP_200_OK)
        except (Club.DoesNotExist, KeyError):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['get'])
    def events(self, request, *args, **kwargs):
        first_of_month = datetime.today().replace(day=1)
        events = Event.objects.filter(date__gte=first_of_month , club__school=self.get_object())
        return Response(EventSerializer(data=events, many=True).data, status=status.HTTP_200_OK)

class EventViewset(viewsets.GenericViewSet):
    queryset = Event.objects.all()
    
    @action(detail=True, methods=['get'])
    def info(self, request, *args, **kwargs):
        email = self.request.query_params.get('email', None)
        district = District.match_district(email)

        if email is not None:
            event: Event = self.get_object()
            try:
                if district == event.club.district:
                    event.send_info(email)
                    return Response({}, status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                pass
        return Response({'message': 'The email provided was invalid or is not allowed to access'}, status=status.HTTP_406_NOT_ACCEPTABLE)


