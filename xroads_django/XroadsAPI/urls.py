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
from XroadsAPI import views, admin_views
from rest_framework_nested import routers

app_name = "api"

router = routers.SimpleRouter(trailing_slash=True)
# ----- Normal Routes
# user/
router.register('user', views.UserViewset, basename="user")

# district/
router.register('district', admin_views.DistrictViewset, basename="district")


# ----- ADMIN ROUTES
# admin/user/
router.register(r'admin/user', admin_views.UserViewset, basename="admin-user")


# admin/district/
router.register('admin/district', admin_views.DistrictViewset,
                basename="admin-district")

# admin/district/school/
admin_school_router = routers.NestedDefaultRouter(router, "admin/district", lookup=r"district")
admin_school_router.register('school', admin_views.SchoolViewset, basename="school")

# admin/district/school/club/
admin_club_router = routers.NestedDefaultRouter(admin_school_router, 'school', lookup=r"school")
admin_club_router.register('club', admin_views.ClubViewset, basename='club')



urlpatterns = [
    path('csrf/', views.csrf),
    re_path("", include(router.urls)),
    re_path("", include(admin_school_router.urls)),
    re_path("", include(admin_club_router.urls)),
]
