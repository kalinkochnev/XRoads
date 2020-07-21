from django.shortcuts import render
from rest_framework import generics

from rest_framework.generics import get_object_or_404
from XroadsAPI.serializers import *

# Create your views here.
def csrf(request):
    return render(request, template_name='home.html')

class GetProfile(generics.RetrieveAPIView):
    model = Profile
    serializer_class = ProfileSerializer

    def get_object(self):
        if 'pk' in self.kwargs.keys():
            return get_object_or_404(Profile, id=self.kwargs['pk'])
        elif 'email' in self.kwargs.keys():
            return get_object_or_404(Profile, user__email=self.kwargs['email'])
    


