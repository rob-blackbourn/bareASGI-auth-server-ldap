"""
Server
"""

import asyncio
import logging
import logging.config

from bareasgi import Application
from hypercorn.asyncio import serve
from hypercorn.config import Config as HypercornConfig

from .app import make_application
from .config import Config

LOGGER = logging.getLogger(__name__)


def start_http_server(app: Application, config: Config) -> None:
    """Start the hypercorn ASGI server"""

    web_config = HypercornConfig()
    web_config.bind = [f'{config.app.host}:{config.app.port}']

    if config.tls.is_enabled:
        web_config.keyfile = config.tls.keyfile
        web_config.certfile = config.tls.certfile

    asyncio.run(
        serve(
            app,  # type: ignore
            web_config
        )
    )


def start_server() -> None:
    config = Config()
    app = make_application(config)
    start_http_server(app, config)
    logging.shutdown()
