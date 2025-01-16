from src.application.exceptions.user import FailedToAuthorize
from src.domain.exceptions import UserNotFound
from src.domain.entities import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.jwt import JWTDecoder, InvalidToken


class UserService:
    def __init__(self,
                 user_repository: UserRepository):
        self.__repository = user_repository

    async def add(self, user: User):
        try:
            inserted_user = await self.__repository.create(user)
            return inserted_user
        except Exception as e:
            print(e)

    async def authorize_user(self, token: str):
        try:
            payload = JWTDecoder.decode(token)
            if not payload.get('sub'):
                raise InvalidToken('Invalid token payload')
            user = await self.__repository.get(payload['sub'])
            return user
        except InvalidToken as e:
            raise FailedToAuthorize(e)
