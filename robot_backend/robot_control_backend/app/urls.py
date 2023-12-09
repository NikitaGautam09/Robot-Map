# app/urls.py

from django.urls import path
from .views import index, add_mission,websocket_handler

urlpatterns = [
    path('', index, name='index'),
    path('add-mission/', add_mission, name='add_mission'),
    path('ws/<int:mission_id>/', websocket_handler, name='websocket_handler'),
]
