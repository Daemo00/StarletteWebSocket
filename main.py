import logging

import uvicorn
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.responses import HTMLResponse
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.INFO,
    )
    root_logger = logging.root
    for uv_logger_name in uvicorn.config.LOGGING_CONFIG['loggers'].keys():
        uv_logger = logging.getLogger(uv_logger_name)
        uv_logger.parent = root_logger


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class Homepage(HTTPEndpoint):
    async def get(self, request):
        return HTMLResponse(html)


class WSEndpoint(WebSocketEndpoint):
    encoding = "text"
    ws_list = list()

    async def on_connect(self, websocket: WebSocket):
        await super().on_connect(websocket)
        self.ws_list.append(websocket)

        logging.info(f"Connected: {websocket}, there are {len(self.ws_list)}")

    async def on_receive(self, websocket: WebSocket, data):
        logging.info(f"Received {data} from {websocket}")

        for ws in self.ws_list:
            ws_name = str(websocket)
            message = f"{ws_name} wrote '{data}'"
            await ws.send_text(message)
            logging.info(f"Message '{data}' sent from {str(websocket)} to {str(ws)}")

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        logging.info(f"Disconnected: {websocket}")
        self.ws_list.remove(websocket)


instance = Starlette(
    routes=(
        Route("/", Homepage, name="Home"),
        WebSocketRoute("/ws", WSEndpoint, name="ws"),
    ),
)

if __name__ == '__main__':
    setup_logging()
    uvicorn.run(instance)
