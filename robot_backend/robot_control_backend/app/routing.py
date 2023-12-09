# backend/app/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .views import websocket_handler

websocket_urlpatterns = [
    path('ws/<int:mission_id>/', websocket_handler),
]


