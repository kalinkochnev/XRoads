from XroadsAPI.models import *
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from XroadsAPI.serializers import *
from rest_framework.response import Response
from collections import OrderedDict
from XroadsAPI.permissions import *
from XroadsAPI.serializers import *
from rest_framework.permissions import IsAuthenticated

class UserViewset(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        return get_object_or_404(Profile, pk=self.kwargs[self.lookup_field])

    def get_serializer(self, *args, **kwargs):
        user: Profile = self.request.user

        requested_user = self.get_object()
        min_admin_role = Role.from_start_model(requested_user.school)

        if min_admin_role.is_allowed(user=user):
            return ProfileSerializer()
        else:
            return AnonProfileSerializer()


class SchoolViewSet(viewsets.GenericViewSet):
    def get_object(self):
        return get_object_or_404(School, id=self.kwargs['school'])

    #@action(detail=True, methods=['get'], hier_perm=HierPerms(min=PermConst.SCHOOL_ADMIN, perms=['create-club']))
    def create_club(self):
        self
        return Response(data=OrderedDict({'hello'}))
    


class GetProfile(generics.UpdateAPIView):
    model = Profile
    serializer_class = ProfileSerializer

    def get_object(self):
        return get_object_or_404(Profile, id=self.kwargs['pk'])

    def check_object_permissions(self, request, obj):
        return super().check_object_permissions(request, obj)
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
    serializer_class = DistrictAdminSerializer

    def get_object(self):
        return get_object_or_404(District, id=self.kwargs['district'])

class CreateClub(generics.CreateAPIView):
    model = Club
    serializer_class = ClubDetailSerializer

# Actions ------
class AddEditor(APIView):
    pass

class RemoveEditor(APIView):
    pass

class CreateClub(APIView):
    pass

class AddSchoolAdmin(APIView):
    pass

class RemoveSchoolAdmin(APIView):
    pass

class AddSchool(APIView):
    pass

class HideSchool(APIView):
    pass

