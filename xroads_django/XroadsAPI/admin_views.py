from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from XroadsAPI.serializers import *

class ClubEditViewset(mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    serializer_class = ClubDetailSerializer
    queryset = Club.objects.all()
    permission_classes = [IsAuthenticated]