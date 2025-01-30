from uuid import UUID

from src.domain.entities import Card, CardStatus
from src.domain.entities.card import SharingURL, CardCopy
from src.domain.repositories.card_repository import CardRepository
from src.infrastructure.rabbitmq.client import RabbitMQClient
from src.infrastructure.utils import generate_share_token


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

    async def create_copy(self, card: Card, original_id: UUID) -> Card:
        created = await self._card_repository.create(card)
        copy = CardCopy(card_id=original_id,
                        copier_id=card.user_id)
        await self._card_repository.create_card_copy(copy)
        return created

    async def start_calculation(self, card: Card) -> Card:
        card.status = CardStatus.PENDING
        updated = await self._card_repository.update(card)
        await self._rabbitmq_client.publish_card(updated)
        return updated

    async def get_by_id(self, card_id: UUID) -> Card:
        card = await self._card_repository.get(card_id)
        return card

    async def get_by_sharing_code(self, code: str) -> Card:
        card = await self._card_repository.get_by_sharing_code(code)
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

    async def create_sharing_url(self, card: Card, base_url: str) -> SharingURL:
        code = generate_share_token()
        url = f'{base_url}?code={code}'
        sharing_url = SharingURL(card_id=card.id,
                                 base_url=base_url,
                                 code=code,
                                 url=url,
                                 user_id=card.user_id)
        created = await self._card_repository.create_sharing_url(sharing_url)
        return created

    async def get_sharing_url_by_card_id(self, card_id: UUID) -> SharingURL:
        card = await self._card_repository.get_sharing_url_by_card_id(card_id)
        return card

    async def get_card_copy(self, card_id: UUID, user_id: UUID) -> Card:
        return await self._card_repository.get_card_copy(card_id, user_id)
