# app/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Mission
from .utils import read_coordinates_from_file
from django.db import IntegrityError
import asyncio
import json
import websockets

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def add_mission(request):
    if request.method == 'POST':
        try:
            mission_number = request.POST.get('mission_number')
        except ValueError:
            return JsonResponse({'status': 'Invalid mission number'})

        try:
            mission = Mission.objects.create(mission_number=mission_number)
            mission.save()

            # Read coordinates from the corresponding .txt file
            file_path = f'mission1.txt'
            coordinates = read_coordinates_from_file(file_path)

            # Send coordinates through WebSocket
            channel_layer = get_channel_layer()
            for coord in coordinates:
                async_to_sync(channel_layer.group_send)(
                    f'mission_{mission.id}',
                    {
                        'type': 'robot_coordinates',
                        'latitude': coord['latitude'],
                        'longitude': coord['longitude'],
                    }
                )

            return JsonResponse({'status': 'Mission added successfully'})
        except IntegrityError:
            return JsonResponse({'status': 'Mission with this number already exists'})
    return JsonResponse({'status': 'Failed to add mission'})

# @csrf_exempt
# def add_mission(request):
#     if request.method == 'POST':
#         mission_number = request.POST.get('mission')
#         mission = Mission.objects.create(mission_number=mission_number)
#         mission.save()

#         # Read coordinates from the corresponding .txt file
#         file_path = f'mission1.txt'
#         coordinates = read_coordinates_from_file(file_path)

#         # Send coordinates through WebSocket
#         channel_layer = get_channel_layer()
#         for coord in coordinates:
#             async_to_sync(channel_layer.group_send)(
#                 f'mission_{mission.id}',
#                 {
#                     'type': 'robot_coordinates',
#                     'latitude': coord['latitude'],
#                     'longitude': coord['longitude'],
#                 }
#             )

#         return JsonResponse({'status': 'Mission added successfully'})
#     return JsonResponse({'status': 'Failed to add mission'})
# async def websocket_handler(websocket, path):
#     mission_id = int(path.strip("/"))
#     mission = Mission.objects.get(id=mission_id)

#     # Read coordinates from the corresponding .txt file
#     file_path = f'./mission1.txt'
#     coordinates = read_coordinates_from_file(file_path)

#     for coord in coordinates:
#         await websocket.send(json.dumps({
#             'latitude': coord['latitude'],
#             'longitude': coord['longitude'],
#         }))

#     await websocket.close()
async def websocket_handler(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    print(f"test")

    # Simulate generating dummy coordinates
    async def generate_dummy_coordinates():
        for i in range(10):
            yield {
                'latitude': 10.0 + i * 0.1,
                'longitude': 20.0 + i * 0.2,
            }
            await asyncio.sleep(1)  # Simulate a delay of 1 second between coordinates

    websocket = websockets.WebSocketResponse()
    await websocket.prepare(request)

    async for coord in generate_dummy_coordinates():
        await websocket.send_json(coord)

    await websocket.close()
    return websocket

