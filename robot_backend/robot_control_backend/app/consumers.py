# backend/app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RobotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.mission_id = self.scope['url_route']['kwargs']['mission_id']
        self.room_group_name = f'mission_{self.mission_id}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'robot_coordinates',
                'latitude': latitude,
                'longitude': longitude,
            }
        )

    # Receive message from room group
    async def robot_coordinates(self, event):
        latitude = event['latitude']
        longitude = event['longitude']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'latitude': latitude,
            'longitude': longitude,
        }))
