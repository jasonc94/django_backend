from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="participants"
    )
    joinedAt = models.DateTimeField(auto_now_add=True)
    leftAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
