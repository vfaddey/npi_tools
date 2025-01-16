from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class CardStatus(str, Enum):
    PENDING = "pending"
    FAILED = "failed"
    COMPLETE = "complete"


@dataclass
class Card:
    file_id: Optional[UUID] = None
    card_type: Optional[str] = None
    id: Optional[UUID] = None
    markdown_text: Optional[str] = None
    status: Optional[CardStatus] = None
    user_id: Optional[UUID] = None
    result: Optional[dict] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def dump(self):
        return asdict(self)
