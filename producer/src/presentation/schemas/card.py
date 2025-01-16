from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4

from src.domain.entities import CardStatus


class CreateCardSchema(BaseModel):
    file_id: UUID4
    card_type: str


class CardSchema(BaseModel):
    id: UUID4
    file_id: UUID4
    card_type: str
    markdown_text: str
    status: CardStatus
    user_id: UUID4
    result: Optional[dict] = None

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UpdateCardSchema(BaseModel):
    id: UUID4
    markdown_text: Optional[str] = None

