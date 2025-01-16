from fastapi import APIRouter, Depends

from src.domain.entities import User
from src.presentation.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get('/me')
async def get_me(user: User = Depends(get_current_user)):
    return user