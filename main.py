from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response


class HelloEndpoint(HTTPEndpoint):
    def get(self, request: Request):
        return Response("<h1>Hello, World!</h1>")


instance = Starlette(
    routes=(
        Route("/hello", HelloEndpoint, name="hello"),
    ),
)
