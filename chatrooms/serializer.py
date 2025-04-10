from chatrooms.models import Room, Participant
from rest_framework import serializers


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id", "name", "joinedAt", "leftAt"]


class RoomSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["id", "name", "createdAt", "participants"]
        extra_kwargs = {"createdAt": {"read_only": True}}
