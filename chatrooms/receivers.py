import datetime
from django.dispatch import receiver
from .signals import user_joined_room, user_left_room
from .models import Participant, Room, User
from django.utils import timezone


@receiver(user_joined_room)
def handle_user_join(sender, user_id, user_display_name, room_name, **kwargs):
    room, _ = Room.objects.get_or_create(name=room_name)
    user, _ = User.objects.get_or_create(
        userId=user_id, defaults={"name": user_display_name}
    )

    if user.name != user_display_name:
        user.name = user_display_name
        user.save()

    participant, created = Participant.objects.get_or_create(user=user, room=room)

    if not created:
        participant.joinedAt = timezone.now()
        participant.leftAt = None
        participant.save()


@receiver(user_left_room)
def handle_user_leave(sender, user_id, user_display_name, room_name, **kwargs):
    try:
        room = Room.objects.get(name=room_name)
        user = User.objects.get(userId=user_id)
        Participant.objects.filter(user=user, room=room).update(leftAt=timezone.now())
    except (Room.DoesNotExist, User.DoesNotExist):
        print(f"User or room not found for: {user_display_name} / {room_name}")
