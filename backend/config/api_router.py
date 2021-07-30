from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

from api import views, admin_views


router.register(r'club', views.ClubViewset)
router.register(r'school', views.SchoolViewset)
router.register(r'district', views.DistrictViewset)
router.register(r'events', views.EventViewset)

router.register(r'club/(?P<code>[a-z0-9A-Z]+)', admin_views.ClubEditViewset)
router.register(r'event/(?P<club_slug>[^/.]+)/(?P<code>[a-z0-9A-Z]+)', admin_views.EventViewset)

app_name = "api"
urlpatterns = router.urls + [path('csrf/', views.csrf)]
