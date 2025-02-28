from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from app.card_handlers.base.card_handler import HandlerResult


class CardType(str, Enum):
    PSEUDOSOIL = 'pseudosoil'


class CardStatus(str, Enum):
    CREATED = 'created'
    FAILED = 'failed'
    PENDING = 'pending'
    COMPLETE = 'complete'


@dataclass
class Card:
    id: str | int | UUID
    created_at: datetime
    file_id: UUID
    status: CardStatus
    user_id: UUID
    card_type: str
    result: Optional[dict | HandlerResult]

    def dump(self):
        return asdict(self)
