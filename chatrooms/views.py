from rest_framework import viewsets
from chatrooms.serializer import RoomSerializer
from .models import Participant, Room
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import models


# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Room.objects.prefetch_related(
        models.Prefetch(
            "participants", queryset=Participant.objects.filter(leftAt__isnull=True)
        )
    )
    serializer_class = RoomSerializer
