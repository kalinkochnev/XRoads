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

class AdminViewset(viewsets.GenericViewSet):
    pass

class UserViewset(viewsets.GenericViewSet, generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, MinSchoolAdminForUser]
    serializer_class = ProfileSerializer
    lookup_field = 'pk'
    hier_perms = ['view-user-detail']
    queryset = Profile

    def retrieve(self, request, *args, **kwargs):
        self.check_permissions(request)
        return super().retrieve(request, *args, **kwargs)

class DistrictViewset(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer