import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import PlainTextResponse, StreamingResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from tools.helpers import take_screenshot


async def get_ip(request: Request) -> PlainTextResponse:
    return PlainTextResponse(request.client.host)


async def get_screenshot(request: Request) -> StreamingResponse:
    url = request.path_params['url']
    screen = await take_screenshot(f'https://{url}')
    return StreamingResponse(screen)


app = Starlette(
    routes=(
        Route('/', get_ip),
        Route('/screen/{url:path}', get_screenshot),
    ),
    middleware=(
        Middleware(CORSMiddleware, allow_origins=('https://ipaddress.su',)),
    ),
)


if __name__ == '__main__':
    uvicorn.run('app:app', port=8001, host='::1', forwarded_allow_ips='::')
