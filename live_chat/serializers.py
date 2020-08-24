from rest_framework import serializers

from live_chat import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = (
            "participants",
            "messages"
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = (
            "sender_id",
            "sent_date",
            "content"
        )
