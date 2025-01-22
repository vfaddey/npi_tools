from uuid import UUID

from src.application.exceptions.base import NPIToolsException
from src.application.exceptions.groups import NotAGroupOwner
from src.application.services.group_service import GroupService
from src.domain.entities import Group


class GetGroupsUseCase:

    def __init__(self, group_service: GroupService):
        self.group_service = group_service


    async def execute(self, user_id: UUID) -> list[Group]:
        return await self.group_service.get_by_user_id(user_id)


class DeleteGroupUseCase:
    def __init__(self, group_service: GroupService):
        self.group_service = group_service

    async def execute(self, group_id: UUID, user_id: UUID) -> Group:
        return await self.group_service.delete(group_id, user_id)


class RenameGroupUseCase:

    def __init__(self, group_service: GroupService):
        self.group_service = group_service

    async def execute(self, group_id: UUID, new_name: str, user_id: UUID) -> Group:
        group_ex = await self.group_service.get_by_id(group_id)
        if group_ex.user_id != user_id:
            raise NotAGroupOwner('You are not allowed to rename this group')
        if group_ex.name == new_name:
            raise NPIToolsException('The name you provided is equal to current')
        return await self.group_service.rename_group(group_id, new_name)