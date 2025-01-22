from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from starlette import status

from src.application.exceptions.base import NPIToolsException
from src.application.exceptions.groups import NotAGroupOwner
from src.application.use_cases.groups import GetGroupsUseCase, RenameGroupUseCase, DeleteGroupUseCase, \
    CreateGroupUseCase
from src.domain.entities import User
from src.domain.exceptions import GroupNotFound
from src.presentation.api.deps import get_current_user, get_groups_use_case, get_rename_group_use_case, \
    get_delete_group_use_case, get_create_group_use_case
from src.presentation.schemas.group import GroupSchema, RenameGroupSchema, CreateGroupSchema

router = APIRouter(prefix='/groups', tags=['groups'])



@router.post('',
             response_model=GroupSchema,
             status_code=status.HTTP_201_CREATED,
             description='Создать группу')
async def create_group(group: CreateGroupSchema,
                       user: User = Depends(get_current_user),
                       use_case: CreateGroupUseCase = Depends(get_create_group_use_case)):
    try:
        result = await use_case.execute(group.name, user.id)
        return result
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('',
            response_model=list[GroupSchema],
            description='Получить список групп карточек пользователя')
async def get_groups(user: User = Depends(get_current_user),
                     use_case: GetGroupsUseCase = Depends(get_groups_use_case)):
    try:
        result = await use_case.execute(user.id)
        return result
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch('/{group_id}/rename',
              description='Переименовать название карточки (до 100 символов)')
async def rename_group(schema: RenameGroupSchema,
                       user: User = Depends(get_current_user),
                       use_case: RenameGroupUseCase = Depends(get_rename_group_use_case)):
    try:
        updated = await use_case.execute(user_id=user.id, **schema.model_dump())
        return updated
    except GroupNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NotAGroupOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@router.delete('/{group_id}',
               response_model=GroupSchema,
               description='Удаляет группу карточек (карточки тоже удаляются)')
async def delete_group(group_id: UUID4,
                       user: User = Depends(get_current_user),
                       use_case: DeleteGroupUseCase = Depends(get_delete_group_use_case)):
    try:
        deleted = await use_case.execute(group_id, user.id)
        return deleted
    except GroupNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NotAGroupOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))