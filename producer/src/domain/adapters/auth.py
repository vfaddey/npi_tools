from abc import ABC, abstractmethod


class AuthAdapter(ABC):
    def __init__(self,
                 auth_server_url,
                 userinfo_uri):
        self._auth_server_url = auth_server_url
        self._userinfo_uri = userinfo_uri

    @abstractmethod
    def get_userinfo(self, token):
        raise NotImplementedError
