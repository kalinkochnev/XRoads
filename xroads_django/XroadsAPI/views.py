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
