# robot_control_backend/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from app.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
