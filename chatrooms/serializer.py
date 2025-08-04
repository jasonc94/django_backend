from chatrooms.models import Room, Participant, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "userId"]


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ["user", "joinedAt", "leftAt"]


class RoomSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(
        source="room_participants", many=True, read_only=True
    )

    class Meta:
        model = Room
        fields = ["id", "name", "createdAt", "participants"]
        extra_kwargs = {"createdAt": {"read_only": True}}
