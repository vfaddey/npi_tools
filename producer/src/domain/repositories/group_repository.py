from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.group import Group


class GroupRepository(ABC):

    @abstractmethod
    async def create(self, group: Group) -> Group:
        raise NotImplementedError


    @abstractmethod
    async def get(self, group_id: UUID) -> Group:
        raise NotImplementedError


    @abstractmethod
    async def get_by_ids(self, group_ids: list[UUID]) -> list[Group]:
        raise NotImplementedError


    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Group]:
        raise NotImplementedError


    @abstractmethod
    async def update_name(self, group_id: UUID, group: Group) -> Group:
        raise NotImplementedError


    @abstractmethod
    async def update(self, group: Group) -> Group:
        raise NotImplementedError


    @abstractmethod
    async def delete(self, group_id: UUID) -> Group:
        raise NotImplementedError