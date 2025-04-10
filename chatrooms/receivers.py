import datetime
from django.dispatch import receiver
from .signals import user_joined_room, user_left_room
from .models import Participant, Room
from django.utils import timezone


@receiver(user_joined_room)
def handle_user_join(sender, user, room_name, **kwargs):
    room, created = Room.objects.get_or_create(name=room_name)
    if not room.participants.filter(name=user).exists():
        room.participants.create(name=user)
    else:
        room.participants.filter(name=user).update(leftAt=None)


@receiver(user_left_room)
def handle_user_leave(sender, user, room_name, **kwargs):
    try:
        room = Room.objects.get(name=room_name)
        room.participants.filter(name=user).update(leftAt=timezone.now())
    except Room.DoesNotExist:
        print(f"room {room_name} doesn't exist")
        return
