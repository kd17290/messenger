# In routing.py
from channels.routing import route

from msgr.consumers import ws_add, ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add, path=r"/message-updates/(?P<user_id>[0-9]+)/$"),
    route("websocket.disconnect", ws_disconnect, path=r"/message-updates/(?P<user_id>[0-9]+)/$"),
]