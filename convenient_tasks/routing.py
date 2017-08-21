from channels import route

from problems import consumers

channel_routing = [
    route('websocket.connect', consumers.ws_connect, path=r'^/problems/tasks/'),
    route('websocket.receive', consumers.ws_message, path=r'^/problems/tasks/'),
    # route('websocket.receive', consumers.pb_test_connect, path=r'^/problems/index/')
]