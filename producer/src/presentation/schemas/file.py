from pydantic import BaseModel
from pydantic import UUID4


class UploadFileResponse(BaseModel):
    id: UUID4