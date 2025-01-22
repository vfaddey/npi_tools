from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4
from src.presentation.schemas.card import CardSchema


class CreateGroupSchema(BaseModel):
    name: str


class RenameGroupSchema(BaseModel):
    new_name: str
    group_id: UUID4


class GroupSchema(BaseModel):
    id: UUID4
    name: str
    user_id: UUID4
    cards: list[CardSchema]

    created_at: Optional[datetime]
    updated_at: Optional[datetime]