from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from app.card_handlers.base.card_handler import HandlerResult


class CardType(Enum):
    PVT = 'pvt'


class CardStatus(str, Enum):
    FAILED = 'failed'
    PENDING = 'pending'
    SUCCESS = 'success'


@dataclass
class Card:
    id: str | int | UUID
    created_at: datetime
    file_id: UUID
    status: CardStatus
    result: Optional[dict | HandlerResult]
