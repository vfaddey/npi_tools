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
    data_url: str
    status: CardStatus
    result: Optional[dict | HandlerResult]
    message: Optional[str] = None
    error: Optional[str] = None
