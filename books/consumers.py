import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:

            self.group_name = 'notification_request'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def notify(self, event):
        await self.send(text_data=json.dumps(event["text"]))
