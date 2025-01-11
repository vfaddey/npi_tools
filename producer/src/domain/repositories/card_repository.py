from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.card import Card


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
    async def update(self, card: Card) -> Card:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, card_id: UUID):
        raise NotImplementedError
