import uuid

from src.application.services.file_service import FileService
from src.domain.entities import File
from src.domain.entities.card import CardType
from src.infrastructure.minio import BUCKET_NAME


class UploadFileUseCase:
    def __init__(self,
                 file_service: FileService):
        self.file_service = file_service

    async def execute(self, user_id: uuid.UUID, file_data: bytes, filename: str) -> File:
        file = await self.file_service.upload_file(user_id, BUCKET_NAME, file_data, filename)
        return file


class UploadPublicFileUseCase:
    def __init__(self,
                 file_service: FileService):
        self._file_service = file_service

    async def execute(self,
                      user_id: uuid.UUID,
                      file_data: bytes,
                      filename: str,
                      description: str,
                      card_type: CardType = None) -> File:
        file = await self._file_service.upload_file(user_id,
                                                    BUCKET_NAME,
                                                    file_data,
                                                    filename,
                                                    is_public=True,
                                                    description=description,
                                                    template_for=card_type)
        return file