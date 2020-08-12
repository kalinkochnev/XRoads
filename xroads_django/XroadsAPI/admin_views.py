from XroadsAPI.models import *
from rest_framework import generics, viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from XroadsAPI.serializers import *
from rest_framework.response import Response
from collections import OrderedDict
from XroadsAPI.permissions import *
from XroadsAPI.serializers import *
from rest_framework.permissions import IsAuthenticated
from XroadsAPI.forms import *
from XroadsAPI import mixins

# TODO make sure that you set read_only=True on nested fields so then .update() works

class UserViewset(viewsets.GenericViewSet, generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, MinSchoolAdminForUser]
    serializer_class = ProfileSerializer
    lookup_field = 'pk'
    hier_perms = ['view-user-detail']
    queryset = Profile

    def retrieve(self, request, *args, **kwargs):
        self.check_permissions(request)
        return super().retrieve(request, *args, **kwargs)

class DistrictViewset(mixins.ModifyAndReadViewset):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    
    hier_perms = ['']
    permission_classes = [IsAuthenticated, MinDistrictRole]


class SchoolViewset(mixins.ModifyAndReadViewset):
    queryset = School.objects.all()
    serializer_class = SchoolAdminSerializer
    permission_classes = [IsAuthenticated, MinSchoolRole]
    hier_perms = []

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MinDistrictRole], hier_perms=['create-school'])
    def create_school(self, request):
        serializer = SchoolAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MinSchoolRole], hier_perms=['hide-school'])
    def toggle_hide(self, request):
        school = self.get_object()
        school.toggle_hide()
        return Response(status=204)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MinSchoolRole], hier_perms=['add_admin'])
    def hide_school(self, request):
        pass

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MinDistrictRole], hier_perms=['add_admin'])
    def add_admin(self, request):
        return self.add_admins(request, hier_role=PermConst.SCHOOL_ADMIN)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MinDistrictRole], hier_perms=['remove_admin'])
    def remove_admin(self, request):
        return self.remove_admins(request)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MinSchoolRole], hier_perms=['create-club'])
    def create_club(self, request):
        club_serializer = CreateClubForm(data=request.data)
        if club_serializer.is_valid():
            club_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=club_serializer.errors)

class ClubViewset(mixins.ModifyAndReadViewset, mixins.AdminMixin):
    queryset = Club.objects.all()
    serializer_class = ClubEditorSerializer
    permission_classes = [IsAuthenticated, MinClubEditor]
    hier_perms = []

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MinSchoolRole], hier_perms=['hide-club'])
    def toggle_hide(self, request):
        club = self.get_object()
        club.toggle_hide()
        return Response(status=204)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MinClubEditor], hier_perms=['add_admin'])
    def add_club_editor(self, request):
        return self.add_admins(request, hier_role=PermConst.CLUB_EDITOR)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MinSchoolRole], hier_perms=['remove_admin'])
    def remove_club_editor(self, request):
        return self.remove_admins(request)
    