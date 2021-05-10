import asyncio
import os
import aiohttp.web

from lib import fetch_user, fetch_all_users

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))


async def testhandle(request):
    return aiohttp.web.Response(text='Test handle')


async def get_users(request):
    return aiohttp.web.Response(text='Test handle')


def main():
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    app.router.add_route('GET', '/', testhandle)
    app.router.add_route('GET', '/users/', fetch_all_users)
    aiohttp.web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    main()
