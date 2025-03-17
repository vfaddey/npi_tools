from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import UUID4

from src.domain.entities.card import CardType


class UploadFileResponse(BaseModel):
    id: UUID4


class FileSchema(BaseModel):
    id: UUID4
    filename: str
    description: Optional[str] = ''
    is_public: bool
    user_id: UUID4
    uploaded_at: datetime
    template_for: Optional[CardType] = None