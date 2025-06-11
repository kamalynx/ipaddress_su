import uvicorn
from dotenv import dotenv_values
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


cfg = dotenv_values('.env')


async def get_ip(request: Request) -> PlainTextResponse:
    return PlainTextResponse(request.client.host)


app = Starlette(
    routes=(Route('/', get_ip),),
    middleware=(
        Middleware(
            CORSMiddleware,
            allow_origins=cfg.get(
                'CORS_ALLOWED_HOSTS', 'http://127.0.0.1:8000'
            ).split(','),
        ),
    ),
)


if __name__ == '__main__':
    uvicorn.run('app:app', port=8001, host='::1', forwarded_allow_ips='::')
