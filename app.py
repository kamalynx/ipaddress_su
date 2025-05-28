import httpx
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


async def get_ip(request: Request) -> PlainTextResponse:
    return PlainTextResponse(request.client.host)


app = Starlette(
    routes=(
        Route('/', get_ip),
    ),
    middleware=(
        Middleware(CORSMiddleware, allow_origins=('https://ipaddress.su',)),
    ),
)


if __name__ == '__main__':
    uvicorn.run('app:app', port=8001, host='::1', forwarded_allow_ips='::')
