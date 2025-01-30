from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.card import Card, SharingURL, CardCopy


class CardRepository(ABC):

    @abstractmethod
    async def create(self, card: Card) -> Card:
        raise NotImplementedError

    @abstractmethod
    async def get(self, card_id: UUID) -> Card:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Card]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_sharing_code(self, code: str) -> Card:
        raise NotImplementedError

    @abstractmethod
    async def update(self, card: Card) -> Card:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, card_id: UUID):
        raise NotImplementedError


    @abstractmethod
    async def create_sharing_url(self, sharing_url: SharingURL) -> SharingURL:
        raise NotImplementedError

    @abstractmethod
    async def get_sharing_url_by_card_id(self, card_id: UUID) -> SharingURL:
        raise NotImplementedError


    @abstractmethod
    async def get_card_copy(self, card_id: UUID, user_id: UUID) -> Card:
        raise NotImplementedError

    @abstractmethod
    async def create_card_copy(self, card_copy: CardCopy) -> CardCopy:
        raise NotImplementedError