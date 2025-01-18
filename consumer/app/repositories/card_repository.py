from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.card import Card
from app.exceptions.card import CardNotFound
from app.models.card import CardModel


class CardRepository(ABC):
    @abstractmethod
    async def update(self, card):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, card_id: UUID):
        raise NotImplementedError


class SqlaCardRepository(CardRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def update(self, card):
        try:
            stmt = select(CardModel).where(CardModel.id == card.id)
            res = await self._session.execute(stmt)
            card_db = res.scalar()
            if not card_db:
                raise CardNotFound(f'No such card with id {card.id}')

            for field, value in card.dump().items():
                setattr(card_db, field, value)

            await self._session.commit()
            await self._session.refresh(card_db)

            return self.to_entity(card_db)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def get_by_id(self, card_id: UUID):
        stmt = select(CardModel).where(CardModel.id == card_id)
        result = await self._session.execute(stmt)
        return self.to_entity(result.scalar())

    @staticmethod
    def to_entity(card_db: CardModel):
        return Card(id=card_db.id,
                    file_id=card_db.file_id,
                    status=card_db.status,
                    user_id=card_db.user_id,
                    result=card_db.result,
                    card_type=card_db.card_type,
                    created_at=card_db.created_at)


