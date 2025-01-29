from typing import List
from uuid import UUID

from src.application.exceptions.cards import NotACardOwner
from src.application.exceptions.files import FileNotFound
from src.application.exceptions.groups import NotAGroupOwner
from src.application.services.card_service import CardService
from src.application.services.file_service import FileService
from src.application.services.group_service import GroupService
from src.application.services.user_service import UserService
from src.domain.entities import Card, Group
from src.infrastructure.minio import BUCKET_NAME


class CreateCardUseCase:
    def __init__(self,
                 card_service: CardService,
                 file_service: FileService,
                 group_service: GroupService):
        self._card_service = card_service
        self._file_service = file_service
        self._group_service = group_service

    async def execute(self, card: Card, user_id: UUID) -> Card:
        try:
            if not card.group_id:
                new_group = Group(name=f'Группа {card.card_type}', user_id=user_id)
                new_group = await self._group_service.create(new_group)
                card.group_id = new_group.id
            else:
                group_ex = await self._group_service.get_by_id(card.group_id)
                if group_ex.user_id != user_id:
                    raise NotAGroupOwner('You are not allowed to create card in this group')
                card.group_id = group_ex.id
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
                 file_service: FileService):
        self._card_service = card_service
        self._file_service = file_service

    async def execute(self, card: Card, user_id: UUID) -> Card:
        card_ex = await self._card_service.get_by_id(card.id)
        if card_ex.user_id != user_id:
            raise NotACardOwner('You do not have permission to access this card.')
        if card.name:
            card_ex.name = card.name
        if card.markdown_text:
            card_ex.markdown_text = card.markdown_text
        if card.file_id:
            await self._file_service.get_by_id(card.file_id,
                                                user_id,
                                                BUCKET_NAME)
            card_ex.file_id = card.file_id
        updated = await self._card_service.update(card_ex)
        return updated


class MoveCardUseCase:
    def __init__(self,
                 card_service: CardService,
                 group_service: GroupService):
        self._card_service = card_service
        self._group_service = group_service

    async def execute(self, card_id: UUID, new_group_id: UUID, user_id: UUID) -> Card:
        card_ex = await self._card_service.get_by_id(card_id)
        group_new = await self._group_service.get_by_id(new_group_id)
        if not card_ex.user_id == user_id:
            raise NotACardOwner('You do not have permission to access this card.')
        if not group_new.user_id == user_id:
            raise NotAGroupOwner('You do not have permission to access this card.')
        card_ex.group_id = group_new.id
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


class CalculateCardUseCase:
    def __init__(self,
                 card_service: CardService):
        self._card_service = card_service

    async def execute(self, card_id: UUID, user_id: UUID) -> Card:
        try:
            card_ex = await self._card_service.get_by_id(card_id)
            if not card_ex.file_id:
                raise FileNotFound('There is no file provided to calculate this card.')
            if card_ex.user_id != user_id:
                raise NotACardOwner('You do not have permission to access this card.')
            result = await self._card_service.start_calculation(card_ex)
            return result
        except Exception as e:
            print(e)
            raise e