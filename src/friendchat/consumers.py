import json
from friendchat.models import Channel, Message
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_message(self, message, sender_id):
        sender = User.objects.get(pk=sender_id)
        channel = Channel.objects.get(name=self.room_name)
        new_message = Message.objects.create(sender=sender, channel=channel, content=message)
        new_message.save()
        return new_message

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print("Websocket connected")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        print(message)
        print(sender)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender']
        new_message = await self.create_message(message, sender_id)
        await self.send(text_data=json.dumps({
            'message': new_message.content,
            'sender': new_message.sender.pk
        }))
# class ChatConsumer(AsyncConsumer):
#     def websocket_connect(self, event):
#         print("Connect event is called")

#         self.send({
#             'type': 'websocket.accept'
#         })

#     def websocket_receive(self, event):
#         print(event)
#         self.send({
#             'type': 'websocket.send',
#             'text': event.get('text')
#         })

#     def websocket_disconnect(self, event):
#         print("Connection is disconected")
#         print(event)