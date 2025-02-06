from dataclasses import dataclass, asdict, field
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
    author_id: Optional[UUID] = None
    order: Optional[int] = 0
    result: Optional[dict] = field(default_factory=dict)
    user: Optional['User'] = None
    author: Optional['User'] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self.card_type_translation = CARD_TYPE_TRANSLATIONS.get(self.card_type)

    def dump(self, exclude: Optional[set] = None) -> dict:
        data = asdict(self)
        if exclude:
            for key in exclude:
                data.pop(key, None)
        return data


@dataclass
class SharingURL:
    card_id: UUID
    base_url: str
    code: str
    url: Optional[str]
    user_id: Optional[UUID] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    card: Optional[Card] = None

    def dump(self):
        return {k: v for k, v in asdict(self).items() if k != "card"}


@dataclass
class CardCopy:
    card_id: UUID
    copier_id: UUID

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def dump(self):
        return asdict(self)