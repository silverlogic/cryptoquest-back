from channels.routing import route

channel_routing = [
    route('websocket.connect', 'cryptoquest.consumers.ws_connect'),
    route('websocket.disconnect', 'cryptoquest.consumers.ws_disconnect'),
    route('websocket.receive', 'cryptoquest.consumers.ws_message'),
]
