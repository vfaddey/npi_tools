from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from src.application.exceptions.files import FileNotFound
from src.domain.repositories.file_repository import FileRepository
from src.domain.entities import File
from src.infrastructure.db.models import FileModel


class SqlaFileRepository(FileRepository):
    def __init__(self, session):
        self._session = session

    async def save(self, file: File) -> File:
        file_db = FileModel(
            id=file.id,
            user_id=file.user_id,
            filename=file.filename,
            is_public=file.is_public,
            uploaded_at=file.uploaded_at
        )
        try:
            self._session.add(file_db)
            await self._session.commit()
            await self._session.refresh(file_db)
            return File(id=file_db.id,
                    user_id=file_db.user_id,
                    filename=file_db.filename,
                    is_public=file_db.is_public,
                    uploaded_at=file_db.uploaded_at)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def get_files_by_user(self, user_id: int | UUID) -> list[File]:
        stmt = select(FileModel).where(FileModel.user_id == user_id)
        result = await self._session.execute(stmt)
        files_db = result.unique().scalars().all()
        return [File(id=f.id,
                     user_id=f.user_id,
                     filename=f.filename,
                     is_public=f.is_public,
                     uploaded_at=f.uploaded_at) for f in files_db]

    async def delete(self, file_id: UUID) -> File:
        stmt = delete(FileModel).where(FileModel.id == file_id).returning(FileModel)
        result = await self._session.execute(stmt)
        await self._session.commit()
        file_db = result.scalars().first()
        if not file_db:
            raise FileNotFound(f'No such file with this ID {file_id}')
        return File(id=file_db.id,
                    user_id=file_db.user_id,
                    filename=file_db.filename,
                    is_public=file_db.is_public,
                    uploaded_at=file_db.uploaded_at)

    async def get_by_id(self, file_id: UUID) -> File:
        stmt = select(FileModel).where(FileModel.id == file_id)
        result = await self._session.execute(stmt)
        file_db = result.scalars().first()
        if not file_db:
            raise FileNotFound(f'No such file with this ID {file_id}')
        return File(id=file_db.id,
                    user_id=file_db.user_id,
                    filename=file_db.filename,
                    is_public=file_db.is_public,
                    uploaded_at=file_db.uploaded_at)