from django.urls import path, re_path

from live_chat.consumers import ChatConsumer

# websocket_urlpatterns = [re_path(r"ws/room/(?P<room_id>\w+)/$", ChatConsumer)]
websocket_urlpatterns = [path("ws/room/<int:room_id>/", ChatConsumer)]
