from typing import List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities import Card
from src.domain.entities.card import Card
from src.domain.exceptions.cards import CardNotFound
from src.domain.repositories.card_repository import CardRepository
from src.infrastructure.db.models import CardModel


class SqlaCardRepository(CardRepository):
    def __init__(self, session):
        self._session = session

    async def create(self, card: Card) -> Card:
        card_db = CardModel(**card.dump())
        try:
            self._session.add(card_db)
            await self._session.commit()
            await self._session.refresh(card_db)
            return Card(id=card_db.id,
                        card_type=card_db.card_type,
                        user_id=card_db.user_id,
                        status=card_db.status,
                        markdown_text=card_db.markdown_text,
                        file_id=card_db.file_id,
                        created_at=card_db.created_at,
                        updated_at=card_db.updated_at,
                        result=card_db.result)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def get(self, card_id: UUID) -> Card:
        stmt = select(CardModel).where(CardModel.id == card_id)
        result = await self._session.execute(stmt)
        card_db = result.scalars().first()
        if not card_db:
            raise CardNotFound(f'No such card with id {card_id}')
        return Card(id=card_db.id,
                    card_type=card_db.card_type,
                    user_id=card_db.user_id,
                    status=card_db.status,
                    markdown_text=card_db.markdown_text,
                    file_id=card_db.file_id,
                    created_at=card_db.created_at,
                    updated_at=card_db.updated_at,
                    result=card_db.result)

    async def get_by_user_id(self, user_id: UUID) -> list[Card]:
        stmt = select(CardModel).where(CardModel.user_id == user_id)
        result = await self._session.execute(stmt)
        cards_db = result.unique().scalars().all()
        return [Card(id=card_db.id,
                     card_type=card_db.card_type,
                     user_id=card_db.user_id,
                     status=card_db.status,
                     markdown_text=card_db.markdown_text,
                     file_id=card_db.file_id,
                     created_at=card_db.created_at,
                     updated_at=card_db.updated_at,
                     result=card_db.result) for card_db in cards_db]


    async def update(self, card: Card) -> Card:
        try:
            card_db = await self._session.get(CardModel, card.id)
            if not card_db:
                raise CardNotFound(f'No such card with id {card.id}')

            for field, value in card.dump().items():
                setattr(card_db, field, value)

            await self._session.commit()
            await self._session.refresh(card_db)

            return Card(
                id=card_db.id,
                card_type=card_db.card_type,
                user_id=card_db.user_id,
                status=card_db.status,
                markdown_text=card_db.markdown_text,
                file_id=card_db.file_id,
                created_at=card_db.created_at,
                updated_at=card_db.updated_at,
                result=card_db.result,
            )
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e


    async def delete(self, card_id: UUID):
        stmt = delete(CardModel).where(CardModel.id == card_id).returning(CardModel)
        result = await self._session.execute(stmt)
        await self._session.commit()
        card_db = result.scalars().first()
        if not card_db:
            raise CardNotFound(f'No such card with id {card_id}')
        return Card(id=card_db.id,
                    card_type=card_db.card_type,
                    user_id=card_db.user_id,
                    status=card_db.status,
                    markdown_text=card_db.markdown_text,
                    file_id=card_db.file_id,
                    created_at=card_db.created_at,
                    updated_at=card_db.updated_at,
                    result=card_db.result)
