from src.application.exceptions.user import FailedToAuthorize
from src.domain.exceptions import UserNotFound
from src.application.services.user_service import UserService
from src.domain.adapters import AuthAdapter
from src.domain.entities import User


class GetUserUseCase:
    def __init__(self,
                 user_service: UserService,
                 auth_adapter: AuthAdapter,
                 token: str):
        self.user_service = user_service
        self.auth_adapter = auth_adapter
        self.token = token

    async def execute(self) -> User:
        try:
            user = await self.user_service.authorize_user(self.token)
            return user
        except UserNotFound as e:
            try:
                user_to_add = await self.auth_adapter.get_userinfo(self.token)
                user = await self.user_service.add(user_to_add)
                return user
            except:
                raise e
        except FailedToAuthorize as e:
            raise e