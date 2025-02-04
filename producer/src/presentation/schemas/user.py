from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4


class UserSchemaFull(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: str
    email_verified: bool
    phone_number: str
    phone_number_verified: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserSchemaShort(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
