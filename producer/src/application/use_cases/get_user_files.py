from src.application.services import file_service
from src.application.services.file_service import FileService
from src.domain.entities import File


class GetUserFilesUseCase:
    def __init__(self,
                 file_service: FileService):
        self._file_service = file_service

    async def execute(self, user_id, show_all: bool = False) -> list[File]:
        return await self._file_service.get_user_files(user_id, show_all)