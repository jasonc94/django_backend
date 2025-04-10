from chatrooms.models import Room, Participant
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "name", "createdAt"]
        extra_kwargs = {"createdAt": {"read_only": True}}


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id", "name", "joinedAt", "leftAt"]
