from channels.generic.websocket import AsyncWebsocketConsumer
import json

from chats.models import ChatMessage, Room


# Класс по работе с сообщениями
class ChatConsumer(AsyncWebsocketConsumer):
    # Коннект к каналу TODO посмотреть, мб исправить
    async def connect(self):
        id = self.scope['url_route']['kwargs']['room_name']
        if id.find('_room') == -1:
            peer_id = int(id)
            user_id = self.scope['user'].id

            if peer_id > user_id:
                room_name = str(user_id) + '_' + str(peer_id)
            elif user_id > peer_id:
                room_name = str(peer_id) + '_' + str(user_id)
            else:
                room_name = str(user_id) + '_' + str(user_id)
            self.room_group_name = 'chat_%s' % hash(room_name)
        else:
            self.room_group_name = 'chat_%s' % id

        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name)

    # Обработка сообщения после отпрвки
    async def receive(self, text_data):
        if 'is_read' in text_data:
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': {'status': 'is_read', 'user_id': self.scope['user'].id}
            })
            return

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        id = message['peer_id']
        text = message['text']

        status = 200
        end_message = {
            'status': status,
            'user_id': self.scope['user'].id,
            'text': text,
            'message_id': ''
        }
        if message['edit_message_id']:
            edit_message_answer = ChatMessage.edit_message(self.scope['user'].id, message)
            if edit_message_answer['status'] == 100:  # В случае успеха
                end_message['status'] = edit_message_answer['status']
                end_message['message_id'] = edit_message_answer['message_id']
                await self.channel_layer.group_send(self.room_group_name, {
                    'type': 'chat_message',
                    'message': end_message
                })
                return
            else:  # В случае ошибки
                end_message['status'] = edit_message_answer['status']
                end_message['text'] = edit_message_answer['text']
                await self.channel_layer.group_send(self.room_group_name, {
                    'type': 'chat_message',
                    'message': end_message
                })

        message_db = ChatMessage()
        # Простановка флагов, идет первой, для проверки прав доступа
        dict = ChatMessage.message_flags(self, message)

        if not dict['status'] == '200' or dict['result'] == '-1':
            end_message['status'] = dict['status']
            end_message['text'] = dict['error']
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': end_message
            })
            return

        message_db.flags = dict['result']
        message_db.user = self.scope['user']
        message_db.text = text
        if message['is_room']:
            message_db.room_id = id
        else:
            message_db.peer_id = id
        message_id = message_db.save()
        end_message['message_id'] = message_id

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': end_message
        })

    # Отправка на клиента
    async def chat_message(self, message):
        await self.send(text_data=json.dumps({'message': message}))
