from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

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
            self._session.add(card)
            await self._session.commit()
            await self._session.refresh(card)
            return card
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def get_by_id(self, card_id: UUID):
        stmt = select(CardModel).where(CardModel.id == card_id)
        result = await self._session.execute(stmt)
        return result.scalar()


