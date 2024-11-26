from django.urls import re_path
from .consumers import ReceiveMessageConsumer, SendMessageConsumer

websocket_urlpatterns = [
    re_path(r'ws/receive/$', ReceiveMessageConsumer.as_asgi()),
    re_path(r'ws/send/$', SendMessageConsumer.as_asgi()),
]
