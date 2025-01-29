from dataclasses import dataclass, asdict, Field, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class CardStatus(str, Enum):
    CREATED = "created"
    PENDING = "pending"
    FAILED = "failed"
    COMPLETE = "complete"


class CardType(str, Enum):
    PSEUDOSOIL = 'pseudosoil'
    PVT = 'pvt'

CARD_TYPE_TRANSLATIONS = {
    CardType.PSEUDOSOIL: 'Псевдогрунт',
    CardType.PVT: 'PVT-расчет',
}


@dataclass
class Card:
    name: str = ''
    id: Optional[UUID] = None
    file_id: Optional[UUID] = None
    card_type: Optional[CardType] = None
    card_type_translation: Optional[str] = None
    group_id: Optional[UUID] = None
    markdown_text: Optional[str] = None
    status: Optional[CardStatus] = None
    user_id: Optional[UUID] = None
    result: Optional[dict] = field(default_factory=dict)

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self.card_type_translation = CARD_TYPE_TRANSLATIONS.get(self.card_type)

    def dump(self):
        return asdict(self)
