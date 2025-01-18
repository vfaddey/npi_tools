import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from io import BytesIO
from uuid import UUID, uuid4

from minio import Minio

from app.card_handlers.base.card_handler import HandlerResult
from app.card_handlers.base.exceptions import NoSuchHandler
from app.card_handlers.base.handler_manager import HandlerManager
from app.entities.card import Card, CardStatus, CardType
from app.entities.file import File
from app.exceptions.card import CardNotFound
from app.exceptions.file import FileNotFound, NotAFileOwner
from app.repositories.card_repository import CardRepository, SqlaCardRepository
from app.repositories.file_repository import FileRepository, SqlaFileRepository
from app.core.config import settings


class CardService:
    def __init__(self,
                 card_repository: CardRepository,
                 file_repository: FileRepository,
                 minio_client: Minio,
                 handler_manager: HandlerManager):
        self._card_repository = card_repository
        self._file_repository = file_repository
        self._minio_client = minio_client
        self._handler_manager = handler_manager

    async def process_card(self,
                           id: str,
                           file_id: str,
                           card_type: str):
        try:
            card = await self.get_card_by_id(UUID(id))
            file, data = await self.get_file_by_id(UUID(file_id),
                                             user_id=card.user_id,
                                             bucket_name=settings.MINIO_BUCKET_NAME)
            handler = self._handler_manager.get_handler(card.card_type)
            if card.status == CardStatus.PENDING:
                result = handler.process(data)
                updated_card = await self.__save_result(card, result)
        except CardNotFound as e:
            return None
        except (FileNotFound, NotAFileOwner, NoSuchHandler) as e:
            card.result = {
                'error': {
                    'message': str(e)
                }
            }
            card.status = CardStatus.FAILED
            await self.__save_result(card)


    async def __save_result(self,
                            card: Card,
                            result: HandlerResult = None) -> Card:
        if not result:
            updated = await self._card_repository.update(card)
            return updated

        saved_assets = []
        for asset in result.assets:
            saved_asset = await self.__save_file(user_id=card.user_id,
                                                 bucket_name=settings.MINIO_BUCKET_NAME,
                                                 file_data=asset.data,
                                                 filename=f'some_file{asset.file_format}')
            saved_assets.append(
                {
                    'asset_type': asset.asset_type,
                    'filename': saved_asset.filename,
                    'file_id': str(saved_asset.id),
                }
            )
        res = {
            'data': result.data,
            'assets': saved_assets
        }
        if card.status == CardStatus.PENDING:
            card.status = CardStatus.COMPLETE
        if not card.result or card.result == {}:
            card.result = res
        updated = await self._card_repository.update(card)
        return updated


    async def __save_file(self,
                          user_id: UUID,
                          bucket_name: str,
                          file_data: bytes,
                          filename: str,
                          is_public: bool = False) -> File:
        file_id = uuid4()

        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(
                None,
                self._minio_client.put_object,
                bucket_name,
                str(file_id),
                BytesIO(file_data),
                len(file_data),
                'application/octet-stream'
            )
        except TypeError as e:
            file_data = file_data.getvalue()
            await loop.run_in_executor(
                None,
                self._minio_client.put_object,
                bucket_name,
                str(file_id),
                BytesIO(file_data),
                len(file_data),
                'application/octet-stream'
            )
        file = File(
            id=file_id,
            user_id=user_id,
            filename=filename,
            uploaded_at=datetime.utcnow(),
            is_public=is_public
        )
        await self._file_repository.create(file)
        return file



    async def get_card_by_id(self, card_id: UUID) -> Card:
        return await self._card_repository.get_by_id(card_id)

    async def get_file_by_id(self,
                             file_id: UUID,
                             user_id: UUID,
                             bucket_name) -> (File, BytesIO):
        file = await self._file_repository.get_by_id(file_id)
        if (not file.is_public) and (file.user_id != user_id):
            raise NotAFileOwner('You have not permission to access this file')
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None,
                                              self._minio_client.get_object,
                                              bucket_name,
                                              str(file_id))
            data = BytesIO(data.read())
            data.name = file.filename
            return file, data
        except Exception as e:
            print(e)
            raise e


class CardServiceFactory:
    def __init__(self,
                 session_factory,
                 minio_client,
                 handler_manager):
        self.__session_factory = session_factory
        self.__minio_client = minio_client
        self.__handler_manager = handler_manager

    @asynccontextmanager
    async def get_service(self) -> CardService:
        async with self.__session_factory() as session:
            card_repository = SqlaCardRepository(session)
            file_repository = SqlaFileRepository(session)
            yield CardService(card_repository,
                              file_repository,
                              self.__minio_client,
                              self.__handler_manager)
