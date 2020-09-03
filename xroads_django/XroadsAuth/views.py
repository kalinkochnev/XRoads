from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from dj_rest_auth.views import LoginView
# Create your views here.
def email_confirm_success(request):
    return render(request, 'email_success.html')


class CustomLoginView(LoginView):
    pass