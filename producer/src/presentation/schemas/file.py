from datetime import datetime

from pydantic import BaseModel
from pydantic import UUID4


class UploadFileResponse(BaseModel):
    id: UUID4


class FileSchema(BaseModel):
    id: UUID4
    filename: str
    is_public: bool
    user_id: UUID4
    uploaded_at: datetime