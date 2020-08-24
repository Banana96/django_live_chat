from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from live_chat.models import Room, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    group_name = None

    room = None
    
    @property
    def room_id(self):
        return int(self.scope["url_route"]["kwargs"]["room_id"])

    @property
    def user(self):
        return self.scope["user"]

    def build_event(self, event_type, data=None):
        if data is not None and type(data) is not dict:
            data = {"data": data}

        return {
            "type": event_type,
            **(data or {})
        }

    async def send_to_ws(self, kind, data=None):
        await self.send_json(self.build_event(kind, data))

    async def send_to_group(self, kind, data=None):
        await self.channel_layer.group_send(
            self.group_name,
            {
                **self.build_event(kind, data),
                "user_id": self.user.id
            },
        )

    @database_sync_to_async
    def get_room(self):
        return Room.objects.get(pk=self.room_id)

    @database_sync_to_async
    def can_user_access_room(self):
        return self.user.available_rooms.filter(id=self.room_id).exists()

    @database_sync_to_async
    def get_participants(self):
        qs = self.room.participants.values_list("id", "username")
        return {item[0]: item[1] for item in list(qs)}

    @database_sync_to_async
    def get_last_messages(self, amount=30):
        qs = self.room.messages.order_by("-sent_date")[:amount]
        return list(qs.values("sender_id", "content")[::-1])

    @database_sync_to_async
    def save_message(self, content):
        Message.objects.create(sender=self.user, room=self.room, content=content)

    async def connect(self):
        await self.accept()

        if not self.user.is_authenticated:
            await self.send_json({"error": "Not authenticated"}, close=True)
            return

        try:
            self.room = await self.get_room()
            self.group_name = f"room_{self.room_id}"
        except Room.DoesNotExist:
            await self.send_json({"error": "Invalid room id"}, close=True)
            return

        can_access = await self.can_user_access_room()

        if not can_access:
            await self.send_json({"error": "Not participating"}, close=True)
            return

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.send_to_group("user_joined")

        await self.send_to_ws("init", {
            "user_id": self.user.id,
            "participants": await self.get_participants(),
            "messages": await self.get_last_messages(),
        })

    # Data recieved from group
    async def user_joined(self, json):
        await self.send_to_ws(
            "user_joined",
            {"user_id": json["user_id"]}
        )

    async def user_left(self, json):
        await self.send_to_ws(
            "user_left",
            {"user_id": json["user_id"]}
        )

    async def message_sent(self, json):
        await self.send_to_ws("message_sent", json)

    async def receive_json(self, json, **kwargs):
        """Recieve data from own WebSocket"""
        if "message" in json:
            await self.save_message(json["message"])

            await self.send_to_group(
                "message_sent",
                {"message": json["message"]}
            )

    async def disconnect(self, code):
        await self.send_to_group("user_left",  {"user_id": self.user.id})

        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )
