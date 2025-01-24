from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4

from src.domain.entities import CardStatus
from src.domain.entities.card import CardType


class CreateCardSchema(BaseModel):
    file_id: UUID4
    card_type: CardType
    group_id: Optional[UUID4] = None


class CardSchema(BaseModel):
    id: UUID4
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


class UpdateCardSchema(BaseModel):
    id: UUID4
    markdown_text: Optional[str] = None


class CreateShareUrlSchema(BaseModel):
    base_url: str
    card_id: UUID4
