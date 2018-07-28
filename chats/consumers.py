from channels.generic.websocket import AsyncWebsocketConsumer
import json

from chats.models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        peer_id = int(self.scope['url_route']['kwargs']['room_name'])
        user_id = self.scope['user'].id
        if peer_id > user_id:
            room_name = str(user_id) + '_' + str(peer_id)
        elif user_id > peer_id:
            room_name = str(peer_id) + '_' + str(user_id)
        else:
            room_name = str(user_id) + '_' + str(user_id)

        self.room_group_name = 'chat_%s' % hash(room_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        peer_id = message['peer_id']
        text = message['text']
        status = 200
        end_message = {
            'status': status,
            'user_id': self.scope['user'].id,
            'text': text,
        }
        message_db = ChatMessage()
        # Простановка флагов, идет первой, для проверки прав доступа
        dict = ChatMessage.message_flags(self, message)

        if not dict['status'] == '200':
            end_message['status'] = dict['status']
            end_message['text'] = dict['error']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': end_message
                }
            )
            return

        message_db.flags = dict['result']
        message_db.user = self.scope['user']
        message_db.text = text
        message_db.peer_id = peer_id
        message_db.save()

        # message['time'] = message_db.created  # TODO Разобраться с выводимым временем
        # Send message to WebSocket

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': end_message
            }
        )

    # Receive message from room group
    async def chat_message(self, message):
        await self.send(text_data=json.dumps({
            'message': message
        }))
