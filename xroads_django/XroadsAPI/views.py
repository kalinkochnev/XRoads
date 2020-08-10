from django.shortcuts import render
from rest_framework import generics

from rest_framework.generics import get_object_or_404
from XroadsAPI.serializers import *

# Create your views here.
def csrf(request):
    return render(request, template_name='home.html')

class UserViewset(viewsets.GenericViewSet):
    serializer_class = AnonProfileSerializer
    lookup_field = 'pk'

    @action(detail=True, methods=['get'], permission_classes=[], url_name='basic-detail', url_path='basic-detail')
    def basic_detail(self, request, *args, **kwargs):
        self.check_permissions(self.request)
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(serializer.data)
