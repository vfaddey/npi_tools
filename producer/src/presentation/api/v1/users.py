from fastapi import APIRouter, Depends

from src.domain.entities import User
from src.presentation.api.deps import get_current_user
from src.presentation.schemas.user import UserSchemaFull

router = APIRouter(prefix="/users", tags=["users"])


@router.get('/me',
            response_model=UserSchemaFull,
            description='Данные пользователя')
async def get_me(user: User = Depends(get_current_user)):
    return user