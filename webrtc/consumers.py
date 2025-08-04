import json
from typing import Literal
from channels.generic.websocket import AsyncWebsocketConsumer
from chatrooms.signals import user_joined_room, user_left_room
import asyncio
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async


class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.userId = self.scope["url_route"]["kwargs"]["userId"]

        query_string = self.scope["query_string"].decode()
        query_params = parse_qs(query_string)

        self.displayName = query_params.get("displayName", [self.userId])[0]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_message",
                "payload": {"type": "leave", "userId": self.userId},
                "sender": self.userId,
            },
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        self.signal_user_event("leave")

    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data["type"]
        if type in ["join", "leave"]:
            self.signal_user_event(type)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_message",
                "payload": data,
                "sender": self.userId,
            },
        )

    async def broadcast_message(self, event):
        receiver = event.get("payload", {}).get("receiver")
        if receiver and receiver != self.userId:
            return
        if event["sender"] == self.userId:
            return
        await self.send(
            text_data=json.dumps({"sender": event["sender"], **event["payload"]})
        )

    def signal_user_event(self, event: Literal["join", "leave"]):
        signal = user_joined_room if event == "join" else user_left_room
        asyncio.create_task(
            sync_to_async(signal.send)(
                sender=self,
                user_id=self.userId,
                user_display_name=self.displayName,
                room_name=self.room_group_name,
            )
        )
