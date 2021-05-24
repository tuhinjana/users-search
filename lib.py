import json
import logging

from aiohttp import ClientSession
from aiohttp import TCPConnector
from aiohttp import web
from pydantic import ValidationError

from config import API_TOKEN
from constants import GIT_HUB_BASE_URL
from schema import SingleResponseSchema

logger = logging.getLogger(__name__)


def get_header():
    return { #"Accept": "application/vnd.github.v3+json",
            'Authorization': 'token {}'.format(API_TOKEN)}


async def fetch_all_users(request):
    users_data = []
    name_param = request.rel_url.query['name']
    name_param = name_param.split(',')
    include_param = request.rel_url.query.get('include', None)

    async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        for each_user in name_param:
            url = '{}/users/{}'.format(GIT_HUB_BASE_URL, each_user)

            status, tmp_data = await fetch_data(url, session=session)

            if isinstance(tmp_data, dict):
                tmp_data = {key: val for key, val in tmp_data.items() if key in ('login', 'id', 'url')}
            if status == 200:
                tmp_data['repo_list'] = []
                repo_data = await fetch_public_repos(each_user, session=session)
                for each_repo in repo_data:
                    tmp_repo_data = {}
                    for key, val in each_repo.items():
                        if key in ('id',
                                   'name', 'url',
                                   'created_at',
                                   'updated_at'):
                            tmp_repo_data[key] = val
                    if include_param == 'commit_latest':
                        commit_data = await fetch_last_commit(each_user, each_repo['name'], session=session)
                        tmp_repo_data['commit_latest'] = {key: val for key, val in commit_data.items()
                                                          if key in ('sha', 'commit', 'html_url')}

                    tmp_data['repo_list'].append(tmp_repo_data)

                # logger.info(tmp_data['repo_list'])
            try:
                tmp_data = SingleResponseSchema(**tmp_data)
            except ValidationError as e:
                logger.error(e)
            users_data.append(tmp_data.dict())
        return web.Response(text=str(json.dumps(users_data)), content_type='application/json')


async def fetch_data(url: str, session: ClientSession, **kwargs) -> dict:
    """GET request wrapper to fetch any data from url.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method='GET', url=url, headers=get_header(), timeout=30, **kwargs)
    # resp.raise_for_status()
    logger.info('Got response [%s] for URL: %s', resp.status, url)
    data = await resp.json()
    return resp.status, data


async def fetch_last_commit(user: str, repo_name: str, session: ClientSession,  **kwargs) -> dict:
    """GET request wrapper to fetch last commit details of a repository.

    kwargs are passed to `session.request()`.
    """
    repo_url = '{}/repos/{}/{}/commits/master'.format(GIT_HUB_BASE_URL, user, repo_name)
    resp = await session.request(method='GET', url=repo_url, headers=get_header(), timeout=30, **kwargs)
    resp.raise_for_status()
    logger.info('Got response [%s] for URL: %s', resp.status, repo_url)
    html = await resp.json()
    logger.info(html)
    return html


async def fetch_public_repos(user: str, session: ClientSession, **kwargs) -> dict:
    """GET request wrapper to fetch repo details.

    kwargs are passed to `session.request()`.
    """
    repo_url = '{}/users/{}/repos'.format(GIT_HUB_BASE_URL, user)
    resp = await session.request(method='GET', url=repo_url, headers=get_header(), timeout=30, **kwargs)
    resp.raise_for_status()
    logger.info('Got response [%s] for URL: %s', resp.status, repo_url)
    html = await resp.json()
    logger.info(html)
    return html
