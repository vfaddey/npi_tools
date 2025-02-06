from uuid import UUID

from src.application.exceptions.groups import NotAGroupOwner
from src.domain.entities import Group
from src.domain.repositories.group_repository import GroupRepository


class GroupService:
    def __init__(self, repository: GroupRepository):
        self.__repository = repository

    async def create(self, group: Group) -> Group:
        return await self.__repository.create(group)

    async def get_by_id(self, group_id: UUID) -> Group:
        return await self.__repository.get(group_id)

    async def get_by_ids(self, group_ids: list[UUID]) -> list[Group]:
        return await self.__repository.get_by_ids(group_ids)

    async def get_by_user_id(self, user_id: UUID) -> list[Group]:
        return await self.__repository.get_by_user_id(user_id)

    async def update(self, group: Group) -> Group:
        return await self.__repository.update(group)

    async def rename_group(self, group_id: UUID, new_name: str) -> Group:
        group_ex = await self.__repository.get(group_id)
        group_ex.name = new_name
        updated = await self.__repository.update_name(group_id, group_ex)
        return updated

    async def delete(self, group_id: UUID, user_id: UUID) -> Group:
        group_ex = await self.__repository.get(group_id)
        if group_ex.user_id != user_id:
            raise NotAGroupOwner('You are not allowed to access this group')
        return await self.__repository.delete(group_id)


