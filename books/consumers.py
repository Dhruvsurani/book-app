import json
from channels.generic.websocket import AsyncWebsocketConsumer
#
#
class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notification_%s' % self.room_name
        print(self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print('connect')
#
#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         # print(text_data_json)
#         #
#         # # Send message to room group
#
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'send_notification',
#                 'message': message
#             }
#         )
#
#     # Receive message from room group
#     async def send_notification(self, event):
#         # message = json.loads(event['message'])
#         print(event['message'])
#
#         # Send message to WebSocket
#         await self.send({
#             'type': 'websocket.send',
#             'text': event['message']
#         }),
#
#