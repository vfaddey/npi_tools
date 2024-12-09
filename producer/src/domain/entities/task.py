from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID


class CardType(str, Enum):
    PVT = "pvt"


@dataclass
class Task:
    id: UUID
    file_id: UUID
    file_extension: str
    card_type: CardType
    mongo_id: str
    status: str = "pending"
    result: Optional[str] = None
