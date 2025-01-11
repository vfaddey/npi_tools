from uuid import UUID

from src.application.services.file_service import FileService
from src.infrastructure.minio import BUCKET_NAME


class DeleteFileUseCase:
    def __init__(self,
                 file_service: FileService):
        self._file_service = file_service

    async def execute(self, file_id: UUID, user_id: UUID):
        existing_file, _ = await self._file_service.get_by_id(file_id,
                                                              user_id,
                                                              BUCKET_NAME)
        deleted_file = await self._file_service.delete_by_id(file_id,
                                                             BUCKET_NAME)
        return deleted_file