from typing import List
from uuid import UUID

from src.application.exceptions.cards import NotACardOwner
from src.application.services.card_service import CardService
from src.application.services.file_service import FileService
from src.application.services.user_service import UserService
from src.domain.entities import Card
from src.infrastructure.minio import BUCKET_NAME


class CreateCardUseCase:
    def __init__(self,
                 card_service: CardService,
                 file_service: FileService):
        self._card_service = card_service
        self._file_service = file_service

    async def execute(self, card: Card, user_id: UUID) -> Card:
        try:
            file, _ = await self._file_service.get_by_id(card.file_id,
                                                user_id,
                                                BUCKET_NAME)
            card.user_id = user_id
            result = await self._card_service.create(card)
            return result
        except Exception as e:
            print(e)
            raise e


class GetCardUseCase:
    def __init__(self,
                 card_service: CardService,
                 user_service: UserService):
        self._card_service = card_service
        self._user_service = user_service

    async def execute(self, card_id: UUID, user_id: UUID) -> Card:
        card = await self._card_service.get_by_id(card_id)
        if card.user_id != user_id:
            raise NotACardOwner('You do not have permission to access this card.')
        return card


class GetUserCardsUseCase:
    def __init__(self,
                 card_service: CardService):
        self._card_service = card_service

    async def execute(self, user_id: UUID) -> list[Card]:
        cards = await self._card_service.get_by_user_id(user_id)
        return cards


class UpdateCardUseCase:
    def __init__(self,
                 card_service: CardService,
                 user_service: UserService):
        self._card_service = card_service
        self._user_service = user_service

    async def execute(self, card: Card, user_id: UUID) -> Card:
        card_ex = await self._card_service.get_by_id(card.id)
        if card_ex.user_id != user_id:
            raise NotACardOwner('You do not have permission to access this card.')
        card_ex.markdown_text = card.markdown_text
        updated = await self._card_service.update(card_ex)
        return updated


class DeleteCardUseCase:
    def __init__(self,
                 card_service: CardService,
                 user_service: UserService):
        self._card_service = card_service
        self._user_service = user_service

    async def execute(self, card_id: UUID, user_id: UUID) -> Card:
        card_ex = await self._card_service.get_by_id(card_id)
        if card_ex.user_id != user_id:
            raise NotACardOwner('You do not have permission to access this card.')
        deleted = await self._card_service.delete(card_id)
        return deleted