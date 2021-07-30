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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from api import views
from api import admin_views

app_name = "api"

default_route = DefaultRouter()
default_route.register(r'club', views.ClubViewset)
default_route.register(r'school', views.SchoolViewset)
default_route.register(r'district', views.DistrictViewset)
default_route.register(r'events', views.EventViewset)

admin_route = DefaultRouter()
admin_route.register(r'club/(?P<code>[a-z0-9A-Z]+)', admin_views.ClubEditViewset)
admin_route.register(r'event/(?P<club_slug>[^/.]+)/(?P<code>[a-z0-9A-Z]+)', admin_views.EventViewset)

urlpatterns = [
    path('', include(default_route.urls)),
    path('', include(admin_route.urls)),
]
