from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    name = models.TextField()
    participants = models.ManyToManyField(
        to=User,
        through="live_chat.Participant",
        related_name="available_rooms"
    )

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    can_moderate = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room} <- {self.user} {'(Mod)' if self.can_moderate else ''}"


class Message(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE, related_name="messages")
    sent_date = models.DateTimeField(auto_now_add=True, null=False)
    removed = models.BooleanField(default=False)
    content = models.TextField()

    def __str__(self):
        return f"{self.sender}@{self.room}: {self.content}"
