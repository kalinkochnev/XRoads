from rest_framework import mixins, viewsets, permissions
from rest_framework.routers import SimpleRouter, Route, DynamicRoute
from XroadsAPI.serializers import *

class IsClubAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Club):
        return request.parser_context['kwargs']['code'] == obj.code

class ClubEditViewset(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    serializer_class = ClubEditSerializer
    queryset = Club.objects.all()
    permission_classes = [IsClubAdmin]
