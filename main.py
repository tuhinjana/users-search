import asyncio
import logging
import os

import aiohttp.web

from lib import fetch_all_users
from logger import AccessLogger

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))


async def test_handle(request):
    return aiohttp.web.Response(text='Test handle')


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    app.router.add_route('GET', '/', test_handle)
    app.router.add_route('GET', '/users/', fetch_all_users)
    aiohttp.web.run_app(app, host=HOST, port=PORT, access_log_class=AccessLogger)


if __name__ == '__main__':
    main()
