from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter, Route, DynamicRoute
from XroadsAPI.serializers import *

class IsClubAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Club):
        return request.parser_context['kwargs']['code'] == obj.code

class ClubEditViewset(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    serializer_class = ClubEditSerializer
    queryset = Club.objects.all()
    permission_classes = [IsClubAdmin, AllowAny]

    @action(detail=True, methods=['post'])
    def toggle_hide(self, request, *args, **kwargs):
        club: Club = self.get_object()
        club.toggle_hide()
        return Response(status=202)
