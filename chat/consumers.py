import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Room, Messages, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        
        if self.user == AnonymousUser():
            await self.close()
            return

        # self.room_group_name = f"chat_{self.user.id}"
        user_ids = sorted([self.user.id, int(self.receiver_id)])
        self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # print(f"✅ WebSocket connected for user {self.user.id} with receiver {self.receiver_id}")

    async def disconnect(self, code):
        return self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]

        receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)

        saved = await self.save_message(receiver, message)

        response = {
            "type": "chat_message",
            "id": saved.id,
            "sender": self.user.id,
            "sender_name": self.user.full_name,
            "receiver": receiver.id,
            "receiver_name": receiver.full_name,
            "content": saved.content,
            "timestamp": saved.timestamp.isoformat(),
        }

        await self.channel_layer.group_send(self.room_group_name, response)

        # await self.channel_layer.group_send(f"chat_{receiver.id}", response)

    async def chat_message(self, event):
        # print(f"📤 Sending to user {self.user.id}: {event}")
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def save_message(self, receiver, message):
        return Messages.objects.create(
            receiver=receiver,
            sender=self.user,
            content=message,
        )
