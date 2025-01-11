import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class User:
    id: UUID
    first_name: str
    last_name: str
    email: str
    email_verified: bool
    phone_number: str
    phone_number_verified: bool
    admin: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def dump(self):
        return asdict(self)
