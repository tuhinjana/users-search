import logging
from aiohttp import ClientSession, TCPConnector
from aiohttp import web
import json

logger = logging.getLogger(__name__)


async def fetch_all_users(request):
    users_data = []
    param1 = request.rel_url.query['name']
    param1 = param1.split(",")
    async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        for each_user in param1:
            url = "https://api.github.com/search/users/?q={}+in:name".format(each_user)
            status, tmp_data = await fetch_user(url, session=session)
            logger.info(tmp_data)
            users_data.append(tmp_data)
        return web.Response(text=str(json.dumps(users_data)))


async def fetch_user(url: str, session: ClientSession, **kwargs) -> dict:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    #resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return resp.status, html


async def fetch_public_repos(user: str, session: ClientSession, **kwargs) -> dict:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """
    repo_url = "https://api.github.com/users/{}/repos".format(user)
    resp = await session.request(method="GET", url=repo_url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, repo_url)
    html = await resp.json()
    return html