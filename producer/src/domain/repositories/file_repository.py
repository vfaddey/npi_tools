from abc import ABC, abstractmethod
from typing import BinaryIO


class FileRepository(ABC):
    @abstractmethod
    async def upload_file(self, file: BinaryIO, file_name: str, content_type: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_file_url(self, file_key: str, expires_in: int = 3600) -> str:
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, file_key: str):
        raise NotImplementedError