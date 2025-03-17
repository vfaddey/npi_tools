from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.entities.card import CardType


@dataclass
class File:
    id: UUID
    filename: str
    uploaded_at: datetime
    is_public: bool
    uploaded_by_user: bool
    user_id: UUID
    description: Optional[str] = ''
    template_for: Optional[CardType] = None

    file_hash: Optional[str] = None

    def dump(self):
        return asdict(self)
