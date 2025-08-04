from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(
        "User", through="Participant", related_name="rooms"
    )

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=255)
    userId = models.CharField(max_length=255, unique=True)
    isGuest = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="room_participants"
    )
    joinedAt = models.DateTimeField(auto_now_add=True)
    leftAt = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "room")

    def __str__(self):
        return f"{self.user.name} in {self.room.name}"
