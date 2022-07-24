
from fastapi import Request
from loguru import logger

from response_api.util.api import time_count, time_second


def init_latency(app):
    @app.middleware("http")
    async def instrumentation(request: Request, call_next):
        _time = time_second()
        response = await call_next(request)
        try:
            path = [
                route for route in request.scope['router'].routes if route.endpoint == request.scope['endpoint']
            ][0].path
        except KeyError:
            path = ''

        if path not in ['/docs', '/openapi.json', '/redoc']:
            logger.log("RESPONSE", f'[*] STATUS: {response.status_code}')
            logger.log("LATENCY", f'[*] {time_count(_time)} s')
        return response
    return app
