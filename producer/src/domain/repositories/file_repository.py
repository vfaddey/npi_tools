from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.file import File


class FileRepository(ABC):
    @abstractmethod
    async def save(self, file: File) -> File:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, file_id: int | UUID) -> File:
        raise NotImplementedError

    @abstractmethod
    async def get_files_by_user(self, user_id: int | UUID):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, file_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get_by_hash_and_user_id(self, file_hash: str, user_id: UUID) -> File:
        raise NotImplementedError