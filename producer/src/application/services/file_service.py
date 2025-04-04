import asyncio
import hashlib
import io
import uuid
from datetime import datetime
from io import BytesIO

from minio import Minio

from src.application.exceptions.files import NotAFileOwner, FileNotFound, FileAlreadyExists
from src.domain.entities.card import CardType
from src.domain.entities.file import File
from src.domain.repositories.file_repository import FileRepository


class FileService:
    def __init__(self,
                 file_repo: FileRepository,
                 minio_client: Minio):
        self.file_repo = file_repo
        self.minio_client = minio_client

    async def upload_file(self,
                          user_id: uuid.UUID,
                          bucket_name: str,
                          file_data: bytes,
                          filename: str,
                          is_public: bool = False,
                          uploaded_by_user: bool = True,
                          description: str = '',
                          template_for: CardType = None) -> File:
        file_id = uuid.uuid4()
        file_hash = hashlib.sha256(file_data).hexdigest()
        try:
            file_ex = await self.file_repo.get_by_hash_and_user_id(file_hash, user_id)
            return file_ex
        except FileNotFound:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self.minio_client.put_object,
                bucket_name,
                str(file_id),
                io.BytesIO(file_data),
                len(file_data),
                'application/octet-stream'
            )
            file = File(
                id=file_id,
                user_id=user_id,
                filename=filename,
                description=description,
                uploaded_at=datetime.utcnow(),
                is_public=is_public,
                uploaded_by_user=uploaded_by_user,
                file_hash=file_hash,
                template_for=template_for
            )
            await self.file_repo.save(file)
            return file

    async def get_by_id(self,
                        file_id: uuid.UUID,
                        user_id: uuid.UUID,
                        bucket_name) -> (File, BytesIO):
        file = await self.file_repo.get_by_id(file_id)
        if (not file.is_public) and (file.user_id != user_id):
            raise NotAFileOwner('You have not permission to access this file')
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None,
                                       self.minio_client.get_object,
                                       bucket_name,
                                       str(file_id))
            data = await loop.run_in_executor(None, response.read)
            response.close()
            return file, data
        except Exception as e:
            print(e)
            raise e

    async def get_user_files(self, user_id: uuid.UUID, show_all: bool):
        files = await self.file_repo.get_files_by_user(user_id, (not show_all))
        return files

    async def get_public_files(self, card_type: CardType = None):
        return await self.file_repo.get_public_files(card_type)

    async def delete_by_id(self,
                           file_id: uuid.UUID,
                           bucket_name: str):
        deleted = await self.file_repo.delete(file_id)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.minio_client.remove_object,
            bucket_name,
            str(file_id),
        )
        return deleted

