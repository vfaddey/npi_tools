from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4, HttpUrl, Field

from src.domain.entities import CardStatus
from src.domain.entities.card import CardType
from src.presentation.schemas.user import UserSchemaShort


class CreateCardSchema(BaseModel):
    card_type: CardType
    name: str
    group_id: Optional[UUID4] = None


class CardSchema(BaseModel):
    id: UUID4
    name: str
    file_id: Optional[UUID4]
    card_type: CardType
    card_type_translation: Optional[str]
    markdown_text: str
    status: CardStatus
    user_id: UUID4
    order: int
    author_id: Optional[UUID4] = None
    group_id: UUID4
    result: Optional[dict] = {}
    user: Optional[UserSchemaShort] = None
    author: Optional[UserSchemaShort] = None

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UpdateCardSchema(BaseModel):
    id: UUID4
    name: Optional[str] = None
    markdown_text: Optional[str] = None
    file_id: Optional[UUID4] = None


class CreateShareUrlSchema(BaseModel):
    base_url: HttpUrl
    card_id: UUID4


class ShareUrlSchema(BaseModel):
    url: HttpUrl
    code: str
    card_id: UUID4

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class MoveCardSchema(BaseModel):
    card_id: UUID4
    group_id: UUID4
    order: int = Field(..., ge=0)
