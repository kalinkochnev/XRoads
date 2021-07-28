from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter, Route, DynamicRoute
from rest_framework.viewsets import GenericViewSet
from api.serializers import *


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


class NoListModelViewset(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    pass


class CanCreateEvent(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            self.club = Club.objects.get(id=request.parser_context['kwargs']['club_id'])
            return self.club.code == request.parser_context['kwargs']['code']
        except Club.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj: Event):
        club = Club.objects.get(id=request.parser_context['kwargs']['club_id'])
        return club == obj.club

class EventViewset(NoListModelViewset):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [CanCreateEvent, AllowAny]

    def get_serializer_context(self):
        club = Club.objects.get(id=self.request.parser_context['kwargs']['club_id'])
        return {'club': club}
    
