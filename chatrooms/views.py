from rest_framework import viewsets
from chatrooms.serializer import RoomSerializer
from .models import Room
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
