from abc import ABC, abstractmethod

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class CardRepository(ABC):
    @abstractmethod
    async def update(self, card):
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


