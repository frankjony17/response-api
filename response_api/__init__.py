__version__ = '1.0.0b9'

from fastapi import FastAPI
from loguru import logger

from response_api.config import init_configuration
from response_api.exception import init_exception
from response_api.router import client, fksolutions, start
from response_api.util.middleware import init_latency


def create_app():
    app = FastAPI(
        title='FkSolutions Response Controller API',
        description='AI response provider for clients like IMA, IBI, FKS',
        version=__version__
    )
    # Init configuration.
    init_configuration()
    # init exception.
    app = init_exception(app)
    # init Latency.
    app = init_latency(app)
    # Add routing.
    app.include_router(fksolutions.route_fksolutions, tags=['Service'])
    app.include_router(client.route_client, tags=['Client'])
    app.include_router(start.start, tags=['Metrics and Health'])
    # Return App.
    logger.info("[+] APPLICATION CREATED, READY TO UP.")
    return app
