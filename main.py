import logging

from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.responses import HTMLResponse
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket

logger = logging.getLogger(__name__)


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

    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()

        logger.info(f"Connected: {websocket}")

    async def on_receive(self, websocket: WebSocket, data):
        await websocket.send_text(f"Message sent was: {data}")

        logger.info("websockets.received")

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        logger.info(f"Disconnected: {websocket}")


instance = Starlette(
    routes=(
        Route("/", Homepage, name="Home"),
        WebSocketRoute("/ws", WSEndpoint, name="ws"),
    ),
)
