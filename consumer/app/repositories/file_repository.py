from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.file import File
from app.exceptions.file import FailedToCreateFile, FileNotFound
from app.models.file import FileModel


class FileRepository(ABC):
    @abstractmethod
    async def create(self, file: File) -> File:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: UUID) -> File:
        raise NotImplementedError


class SqlaFileRepository(FileRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, file: File) -> File:
        file_db = FileModel(**file.dump())
        try:
            self._session.add(file_db)
            await self._session.commit()
            await self._session.refresh(file_db)
            return self.__to_entity(file_db)
        except SQLAlchemyError as e:
            await self._session.rollback()
            print(e)
            raise FailedToCreateFile(f'Failed to create file {file.dump()}')

    async def get_by_id(self, id: UUID) -> File:
        stmt = select(FileModel).where(FileModel.id == id)
        result = await self._session.execute(stmt)
        file_db = result.scalar()
        if not file_db:
            raise FileNotFound(f'File {id} not found')
        return self.__to_entity(file_db)

    @staticmethod
    def __to_entity(file_db: FileModel):
        return File(id=file_db.id,
                    user_id=file_db.user_id,
                    uploaded_at=file_db.uploaded_at,
                    is_public=file_db.is_public,
                    filename=file_db.filename)