import json
from channels.generic.websocket import AsyncWebsocketConsumer


class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.userId = self.scope["url_route"]["kwargs"]["userId"]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         "type": "broadcast_message",
        #         "payload": {"type": "join", "userId": self.userId},
        #         "sender": self.userId,
        #     },
        # )
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

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_message",
                "payload": data,
                "sender": self.userId,
            },
        )

    async def broadcast_message(self, event):
        if event["sender"] == self.userId:
            return
        await self.send(
            text_data=json.dumps({"sender": event["sender"], **event["payload"]})
        )
