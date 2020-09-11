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
from rest_framework_nested import routers

from XroadsAPI import views, admin_views

app_name = "api"

router = routers.SimpleRouter(trailing_slash=True)
# ----- Normal Routes
# user/
# router.register('user', views.UserViewset, basename="user")

# district/
router.register('district', views.DistrictViewset, basename="district")

# district/school/
school_router = routers.NestedDefaultRouter(router, "district", lookup=r"district")
school_router.register('school', views.SchoolViewset, basename="school")

# district/school/club/
club_router = routers.NestedDefaultRouter(school_router, 'school', lookup=r"school")
club_router.register('club', views.ClubViewset, basename='club')


# ----- ADMIN ROUTES
# admin/user/
router.register(r'admin/user', admin_views.UserViewset, basename="admin-user")


# admin/district/
router.register('admin/district', admin_views.DistrictViewset,
                basename="admin-district")

# admin/district/school/
admin_school_router = routers.NestedDefaultRouter(router, "admin/district", lookup=r"district")
admin_school_router.register('school', admin_views.SchoolViewset, basename="admin-school")

# admin/district/school/club/
admin_club_router = routers.NestedDefaultRouter(admin_school_router, 'school', lookup=r"school")
admin_club_router.register('club', admin_views.ClubViewset, basename='admin-club')



urlpatterns = [
    path('csrf/', views.csrf),
    re_path("", include(router.urls)),
    re_path("", include(school_router.urls)),
    re_path("", include(club_router.urls)),
    
    re_path("", include(admin_school_router.urls)),
    re_path("", include(admin_club_router.urls)),
]
