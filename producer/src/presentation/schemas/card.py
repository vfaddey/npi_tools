from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4

from src.domain.entities import CardStatus
from src.domain.entities.card import CardType


class CreateCardSchema(BaseModel):
    file_id: UUID4
    card_type: CardType
    name: str
    group_id: Optional[UUID4] = None


class CardSchema(BaseModel):
    id: UUID4
    name: str
    file_id: UUID4
    card_type: CardType
    card_type_translation: Optional[str]
    markdown_text: str
    status: CardStatus
    user_id: UUID4
    group_id: UUID4
    result: Optional[dict] = {}

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UpdateCardTextSchema(BaseModel):
    id: UUID4
    markdown_text: Optional[str] = None


class MoveCardSchema(BaseModel):
    card_id: UUID4
    group_id: UUID4