from channels import route

from problems import consumers

channel_routing = [
    route('websocket.connect', consumers.ws_connect, path=r'^/problems/tasks/'),
    route('websocket.receive', consumers.ws_search_message, path=r'^/problems/tasks/'),
    route('websocket.connect', consumers.ws_connect, path=r'^/problems/pools/'),
    route('websocket.receive', consumers.ws_pools_message, path=r'^/problems/pools/')
]