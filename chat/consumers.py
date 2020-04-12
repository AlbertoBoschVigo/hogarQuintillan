import json, time
from channels.generic.websocket import AsyncWebsocketConsumer

import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    roomUsers = {}
    roomLog = {}
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        logger.info(f'{self.scope["user"].username} se ha conectado a {self.room_name}')
        self.incluirUsuario(self.scope['user'].username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'users_notification',
                'users': self.roomUsers.get(self.room_group_name),
                'chats': list(self.roomUsers.keys())
            }
            
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        logger.info(f'{self.scope["user"].username} se ha desconectado')
        self.quitarUsuario(self.scope['user'].username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'users_notification',
                'users': self.roomUsers.get(self.room_group_name),
                'chats': list(self.roomUsers.keys())
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
            'users':event['users'],
            'chats':event['chats']
        }))

    def incluirUsuario(self, user):
        _reg = (time.strftime("%H:%M:%S", time.localtime()),user, 'Se ha conectado')
        if self.roomUsers.get(self.room_group_name) is None:
            self.roomUsers[self.room_group_name] = [user]
        else:
            self.roomUsers[self.room_group_name].append(user)

        if self.roomLog.get(self.room_group_name) is None:
            self.roomLog[self.room_group_name] = [_reg]
        else:
            self.roomLog[self.room_group_name].append(_reg)
   
    def quitarUsuario(self, user):
        _reg = (time.strftime("%H:%M:%S", time.localtime()),user, 'Se ha desconectado')
        self.roomUsers[self.room_group_name].remove(user)
        self.roomLog[self.room_group_name].append(_reg)
        if self.roomUsers[self.room_group_name] == []:
            self.roomUsers.pop(self.room_group_name, None)
        