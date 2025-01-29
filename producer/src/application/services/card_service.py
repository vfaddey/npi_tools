from uuid import UUID

from src.domain.entities import Card, CardStatus
from src.domain.repositories.card_repository import CardRepository
from src.infrastructure.rabbitmq.client import RabbitMQClient


class CardService:
    def __init__(self,
                 card_repository: CardRepository,
                 rabbitmq_client: RabbitMQClient):
        self._card_repository = card_repository
        self._rabbitmq_client = rabbitmq_client

    async def create(self, card: Card) -> Card:
        created = await self._card_repository.create(card)
        # await self._rabbitmq_client.publish_card(created)
        return created

    async def start_calculation(self, card: Card) -> Card:
        card.status = CardStatus.PENDING
        updated = await self._card_repository.update(card)
        await self._rabbitmq_client.publish_card(updated)
        return updated

    async def get_by_id(self, card_id: UUID) -> Card:
        card = await self._card_repository.get(card_id)
        return card

    async def get_by_user_id(self, user_id: UUID) -> list[Card]:
        cards = await self._card_repository.get_by_user_id(user_id)
        return cards

    async def update(self, card: Card) -> Card:
        updated = await self._card_repository.update(card)
        return updated

    async def delete(self, card_id: UUID) -> Card:
        deleted = await self._card_repository.delete(card_id)
        return deleted