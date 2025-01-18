from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class CardStatus(str, Enum):
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
    file_id: Optional[UUID] = None
    card_type: Optional[str] = None
    card_type_translation: Optional[str] = None
    id: Optional[UUID] = None
    markdown_text: Optional[str] = None
    status: Optional[CardStatus] = None
    user_id: Optional[UUID] = None
    result: Optional[dict] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self.card_type_translation = CARD_TYPE_TRANSLATIONS.get(self.card_type)
        if not self.card_type_translation:
            raise ValueError(f"Неизвестный тип карточки: {self.card_type}")

    def dump(self):
        return asdict(self)
