from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/squad-connect/(?P<room_name>\w+)/(?P<userId>\w+)/$",
        consumers.WebRTCConsumer.as_asgi(),
    ),
]
