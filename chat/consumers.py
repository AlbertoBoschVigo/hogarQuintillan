import json, time
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    roomUsers = {}
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        self.incluirUsuario(self.scope['user'].username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'users_notification',
                'users': self.roomUsers[self.room_group_name],
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        self.quitarUsuario(self.scope['user'].username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'users_notification',
                'users': self.roomUsers[self.room_group_name],
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope['user'].username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'hour': time.strftime("%H:%M:%S", time.localtime()),
            'user':event['user']
        }))

    async def users_notification(self, event):
        await self.send(text_data=json.dumps({
            'users':event['users']
        }))

    def incluirUsuario(self, user):
        if self.roomUsers.get(self.room_group_name) is None:
            self.roomUsers[self.room_group_name] = [user]
        else:
            self.roomUsers[self.room_group_name].append(user)
   
    def quitarUsuario(self, user):
        self.roomUsers[self.room_group_name].remove(user)