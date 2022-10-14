import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:

            self.group_name = f'notification_request'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    # async def receive(self, text_data=None, bytes_data=None):
    #     # Called with either text_data or bytes_data for each frame
    #     # You can call:
    #     await self.send(text_data="Hello world!")
    #     # Or, to send a binary frame:
    #     await self.send(bytes_data="Hello world!")
    #     # Want to force-close the connection? Call:
    #     await self.close()
    #     # Or add a custom WebSocket error code!
    #     await self.close(code=4123)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def notify(self, event):
        await self.send(text_data=json.dumps(event["text"]))
