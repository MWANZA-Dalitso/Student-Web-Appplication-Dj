import json
from channels.generic.websocket import AsyncWebsocketConsumer  # type: ignore # Import added
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message, Notification

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            self.room_group_name = f'chat_{self.user.username}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        receiver_username = data['receiver']
        receiver = await sync_to_async(User.objects.get)(username=receiver_username)

        message_instance = await self.save_message(self.user, receiver, message)
        await self.create_notification(receiver, message_instance)

        await self.channel_layer.group_send(
            f'chat_{receiver_username}',
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'receiver': receiver_username,
            }
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'receiver': receiver_username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver,
        }))

    @sync_to_async
    def save_message(self, sender, receiver, message):
        return Message.objects.create(sender=sender, receiver=receiver, content=message)

    @sync_to_async
    def create_notification(self, receiver, message):
        return Notification.objects.create(
            user=receiver,
            notification_type='message',
            message=f"New message from {message.sender.username}: {message.content}"
        )
