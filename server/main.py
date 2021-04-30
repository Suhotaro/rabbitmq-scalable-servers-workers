import asyncio
import logging
import uuid

from aiohttp import web

from routes import setup_routes
from rpc import setup_rabbit


log = logging.getLogger(__name__)


async def init_app(loop):
    app = web.Application()

    app["rabbit"] = await setup_rabbit(loop)

    setup_routes(app)

    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app(loop))
    web.run_app(app, host="localhost", port=8080)


async def gunicorn_entrypoint():
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    return await init_app(loop)

if __name__ == '__main__':
    main()
