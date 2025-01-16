import ssl

import aiohttp
import certifi

from src.application.exceptions.base import NPIToolsException
from src.domain.adapters import AuthAdapter
from src.domain.entities import User


class NPIAuthAdapter(AuthAdapter):
    async def get_userinfo(self, token):
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=connector) as session:
                data = await self.__fetch_user(session, token)
                return User(**data)
        except Exception as e:
            print(e)
            raise NPIToolsException('Something went wrong, while getting user data')


    async def __fetch_user(self, session, token: str = None):
        if token:
            headers = {'Authorization': f'Bearer {token}'} if token else {}
            async with session.get(self._auth_server_url + self._userinfo_uri, headers=headers) as response:
                return await response.json()
        async with session.get(self._auth_server_url + self._userinfo_uri) as response:
            return await response.json()

