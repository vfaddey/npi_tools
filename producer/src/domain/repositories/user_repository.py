from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.testing.pickleable import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_id: UUID, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UUID):
        raise NotImplementedError
