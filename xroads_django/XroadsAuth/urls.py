"""xroads_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView
from allauth.account.views import confirm_email
from . import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/success/', views.email_confirm_success, name="account_registration_success"),
    re_path(r"^registration/account-confirm-email/(?P<key>[\s\d\w().+-_',:&]+)/$", confirm_email, name="account_confirm_email"),    
    re_path(r'^registration/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('registration/', include('dj_rest_auth.registration.urls')),
]
