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
from django.urls import path, include
from XroadsAPI import views, admin_views
from rest_framework import routers


admin_urls = [
    # TODO everything in this chunk has not had its views created
    # TODO everything below this point has not had it's permissions setup

    #path('admin/school/<int:school>/create-club/', views.CreateClub.as_view(), name='admin-create-club'),
]
"""path('admin/user/<str:email>/', views.GetProfile.as_view(), name='admin-get-profile'),
path('admin/club/<int:club>/add-editor/<int:user_pk>/', views.AddEditor.as_view(), name='admin-add-editor'),
path('admin/club/<int:club>/remove-editor/<int:user_pk>/', views.RemoveEditor.as_view(), name='admin-add-editor'),
path('admin/school/<int:school>/remove-admin/<int:user_pk>/', views.RemoveSchoolAdmin.as_view(), name="admin-remove-school-admin"),
path('admin/school/<int:school>/add-admin/<int:user_pk>/', views.AddSchoolAdmin.as_view(), name="admin-add-school-admin"),
path('admin/district/<int:district>/add-school/', views.CreateSchool.as_view(), name='admin-create-school'),
path('admin/district/<int:district>/hide-school/', views.CreateSchool.as_view(), name='admin-create-school'),

path('admin/user/', views.ProfileAdmin.as_view(), name='admin-user-detail'),
path('admin/club/<int:club>/', views.ClubEditor.as_view(), name='admin-club-detail'),
path('admin/school/<int:school>/', views.SchoolAdmin.as_view(), name='admin-school-detail'),
path('admin/district/<int:district>/', views.DistrictAdmin.as_view(), name='admin-district-detail'),
"""

urlpatterns = [
    path('csrf/', views.csrf),
    path('club/<int:club>/', views.GetClub.as_view(), name='get-club-detail'),
    path('school/list/', views.GetSchoolList.as_view(), name='get-schools-list'),
    path('school/<int:school>/club-overview/', views.GetClubOverview.as_view(), name='get-club-overview'),
]


router = routers.DefaultRouter()
router.register(r'school', admin_views.SchoolViewSet, basename='school')
urlpatterns += router.urls
