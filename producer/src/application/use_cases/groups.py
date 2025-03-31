from uuid import UUID

from src.application.exceptions.base import NPIToolsException
from src.application.exceptions.groups import NotAGroupOwner
from src.application.services.group_service import GroupService
from src.domain.entities import Group
from src.domain.exceptions import GroupNotFound


class CreateGroupUseCase:
    def __init__(self,
                 group_service: GroupService):
        self._group_service = group_service

    async def execute(self, name: str, user_id: UUID) -> Group:
        groups_ex = await self._group_service.get_by_user_id(user_id)
        order = len(groups_ex)
        group = Group(name=name, user_id=user_id, order=order)
        return await self._group_service.create(group)


class GetGroupsUseCase:

    def __init__(self, group_service: GroupService):
        self.group_service = group_service


    async def execute(self,
                      user_id: UUID,
                      group_ids: list[UUID] = None) -> list[Group]:
        if not group_ids:
            return await self.group_service.get_by_user_id(user_id)
        return await self.group_service.get_by_ids(group_ids)



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


class MoveGroupUseCase:
    def __init__(self, group_service: GroupService):
        self.group_service = group_service

    async def execute(self, group_id: UUID, order: int, user_id: UUID) -> Group:
        if order < 0:
            raise ValueError('Order cannot be negative')
        groups_ex = await self.group_service.get_by_user_id(user_id)
        for idx, group in enumerate(groups_ex):
            if group.id == group_id:
                group_to_move = groups_ex.pop(idx)
                break
        else:
            raise GroupNotFound(f'No such group with id {group_id}')
        if order >= (len(groups_ex) + 1):
            groups_ex.append(group_to_move)
        else:
            groups_ex.insert(order, group_to_move)
        res = None
        for idx, group in enumerate(groups_ex):
            group.order = idx
            if group.id == group_id:
                res = await self.group_service.update(group)
            await self.group_service.update(group)
        return res
