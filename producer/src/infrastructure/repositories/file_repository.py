from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from src.application.exceptions.files import FileNotFound
from src.domain.entities.card import CardType
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
            description=file.description,
            is_public=file.is_public,
            uploaded_by_user=file.uploaded_by_user,
            uploaded_at=file.uploaded_at,
            file_hash=file.file_hash,
            template_for=file.template_for
        )
        try:
            self._session.add(file_db)
            await self._session.commit()
            await self._session.refresh(file_db)
            return self.__to_entity(file_db)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def get_files_by_user(self, user_id: int | UUID, uploaded_by_user: bool) -> list[File]:
        stmt = (select(FileModel)
                .where(FileModel.user_id == user_id, FileModel.uploaded_by_user == uploaded_by_user)
                )
        result = await self._session.execute(stmt)
        files_db = result.unique().scalars().all()
        return [self.__to_entity(f) for f in files_db]

    async def get_public_files(self, card_type: CardType = None):
        stmt = select(FileModel).where(FileModel.is_public == True)
        if card_type:
            stmt = select(FileModel).where(FileModel.is_public == True, FileModel.template_for == card_type)
        result = await self._session.execute(stmt)
        files_db = result.scalars().all()
        return [self.__to_entity(f) for f in files_db]

    async def get_by_hash_and_user_id(self, file_hash: str, user_id: UUID) -> File:
        stmt = select(FileModel).where(FileModel.file_hash == file_hash, FileModel.user_id == user_id)
        result = await self._session.execute(stmt)
        file_db = result.unique().scalars().first()
        if not file_db:
            raise FileNotFound('No file with such hash')
        return self.__to_entity(file_db)

    async def delete(self, file_id: UUID) -> File:
        stmt = delete(FileModel).where(FileModel.id == file_id).returning(FileModel)
        result = await self._session.execute(stmt)
        await self._session.commit()
        file_db = result.scalars().first()
        if not file_db:
            raise FileNotFound(f'No such file with this ID {file_id}')
        return self.__to_entity(file_db)

    async def get_by_id(self, file_id: UUID) -> File:
        stmt = select(FileModel).where(FileModel.id == file_id)
        result = await self._session.execute(stmt)
        file_db = result.scalars().first()
        if not file_db:
            raise FileNotFound(f'No such file with this ID {file_id}')
        return self.__to_entity(file_db)

    def __to_entity(self, file_db: FileModel) -> File:
        return File(id=file_db.id,
                    user_id=file_db.user_id,
                    filename=file_db.filename,
                    description=file_db.description,
                    is_public=file_db.is_public,
                    uploaded_by_user=file_db.uploaded_by_user,
                    uploaded_at=file_db.uploaded_at,
                    file_hash=file_db.file_hash,
                    template_for=file_db.template_for)