from dataclasses import dataclass, Field, asdict, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.entities.card import Card


@dataclass
class Group:
    user_id: UUID
    id: Optional[UUID] = None
    name: Optional[str] = None
    order: Optional[int] = 0
    cards: Optional[list[Card]] = field(default_factory=list)

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def dump(self) -> dict:
        return asdict(self)