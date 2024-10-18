from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.group_name = "progress_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def progress_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'progress_update',
            'progress': event['progress'],
        }))
