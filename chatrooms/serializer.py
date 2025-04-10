from chatrooms.models import Room, Participant


class RoomSerializer:
    class Meta:
        model = Room
        fields = ["id", "name", "createdAt"]
        extra_kwargs = {"createdAt": {"read_only": True}}


class ParticipantSerializer:
    class Meta:
        model = Participant
        fields = ["id", "name", "joinedAt", "leftAt"]
