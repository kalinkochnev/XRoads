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
from rest_framework_nested import routers

router = routers.SimpleRouter()

router.register('admin', admin_views.AdminViewset, basename="admin")

# ----- ADMIN ROUTES
# admin/user/
admin_user_router = routers.NestedSimpleRouter(router, 'admin', lookup='user')
admin_user_router.register('user', admin_views.UserViewset, basename="user")
"""
# admin/district/
admin_district_router = routers.NestedSimpleRouter(router, 'admin', lookup='district')
admin_district_router.register('district', admin_views.DistrictViewset, basename="district")

# admin/district/school/
admin_school_router = routers.NestedSimpleRouter(router, 'district', lookup='district')
admin_school_router.register('school', admin_views.SchoolViewset, basename="school")

# admin/district/school/club/
admin_club_router = routers.NestedSimpleRouter(school_router, 'school', lookup="school")
admin_club_router.register('club', admin_views.ClubViewset, lookup='club')
"""
# ----- NORMAL ROUTES
# user/
router.register('user', UserViewset, basename="user")
"""
# district/
router.register('district', DistrictViewset, basename="district")

# district/school/
school_router = routers.NestedSimpleRouter(router, 'district', lookup='district')
school_router.register('school', SchoolViewset, basename="school")

# district/school/club/admin_views.
club_router = routers.NestedSimpleRouter(school_router, 'school', lookup="school")
club_router.register('club', ClubViewset, lookup='club')
"""

urlpatterns = router.urls

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


"""
path('club/join/<int:club>/, views.JoinClub.as_view())
"""
# urlpatterns = [
# #     path('csrf/', views.csrf),
#     path('club/<int:club>/', views.GetClub.as_view(), name='get-club-detail'),
# #     path('school/list/', views.GetSchoolList.as_view(), name='get-schools-list'),
# #     path('school/<int:school>/club-overview/', views.GetClubOverview.as_view(), name='get-club-overview'),
# #     path('', include(router.urls)),
# ]

# urlpatterns += router.urls