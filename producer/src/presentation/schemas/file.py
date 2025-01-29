from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import UUID4


class UploadFileResponse(BaseModel):
    id: UUID4


class FileSchema(BaseModel):
    id: UUID4
    filename: str
    description: Optional[str] = ''
    is_public: bool
    user_id: UUID4
    uploaded_at: datetime