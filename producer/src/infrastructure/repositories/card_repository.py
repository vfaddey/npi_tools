from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy.testing.plugin.plugin_base import options
from typing_extensions import override

from src.domain.entities import Card, User
from src.domain.entities.card import Card, SharingURL, CardCopy
from src.domain.exceptions.cards import CardNotFound, SharingUrlNotFound, CardCopyNotFound
from src.domain.repositories.card_repository import CardRepository
from src.infrastructure.db.models import CardModel, UserModel
from src.infrastructure.db.models.card import SharingURLModel, CardCopyModel


class SqlaCardRepository(CardRepository):
    def __init__(self, session):
        self._session = session

    @override
    async def create(self, card: Card) -> Card:
        card_db = CardModel(**card.dump(exclude={'user', 'author'}))
        try:
            self._session.add(card_db)
            await self._session.commit()
            await self._session.refresh(card_db)
            return self.__to_entity(card_db)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    @override
    async def get(self, card_id: UUID) -> Card:
        stmt = select(CardModel).where(CardModel.id == card_id)
        result = await self._session.execute(stmt)
        card_db = result.scalars().first()
        if not card_db:
            raise CardNotFound(f'No such card with id {card_id}')
        return self.__to_entity(card_db)

    @override
    async def get_by_user_id(self, user_id: UUID) -> list[Card]:
        stmt = select(CardModel).where(CardModel.user_id == user_id)
        result = await self._session.execute(stmt)
        cards_db = result.unique().scalars().all()
        return [self.__to_entity(card_db) for card_db in cards_db]

    @override
    async def get_by_sharing_code(self, code: str) -> Card:
        stmt = select(SharingURLModel).where(SharingURLModel.code == code)
        result = await self._session.execute(stmt)
        url_db = result.scalars().first()
        if not url_db:
            raise SharingUrlNotFound(f'No such sharing url with code {code}')
        return self.__to_entity(url_db.card)

    @override
    async def update(self, card: Card) -> Card:
        try:
            card_db = await self._session.get(CardModel, card.id)
            if not card_db:
                raise CardNotFound(f'No such card with id {card.id}')

            allowed_fields = {column.name for column in CardModel.__table__.columns}

            for field, value in card.dump().items():
                if field in allowed_fields:
                    setattr(card_db, field, value)

            await self._session.commit()
            await self._session.refresh(card_db)
            return self.__to_entity(card_db)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e


    @override
    async def delete(self, card_id: UUID):
        stmt = delete(CardModel).where(CardModel.id == card_id).returning(CardModel)
        result = await self._session.execute(stmt)
        await self._session.commit()
        card_db = result.scalars().first()
        if not card_db:
            raise CardNotFound(f'No such card with id {card_id}')
        return self.__to_entity(card_db)

    @override
    async def create_sharing_url(self, sharing_url: SharingURL) -> SharingURL:
        try:
            url_db = SharingURLModel(**sharing_url.dump())
            self._session.add(url_db)
            await self._session.commit()
            await self._session.refresh(url_db)
            return self.__to_sharing_url_entity(url_db)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    @override
    async def get_sharing_url_by_card_id(self, card_id: UUID) -> SharingURL:
        stmt = select(SharingURLModel).where(SharingURLModel.card_id == card_id)
        result = await self._session.execute(stmt)
        url_db = result.scalars().first()
        if not url_db:
            raise SharingUrlNotFound(f'No such sharing url with card id {card_id}')
        return self.__to_sharing_url_entity(url_db)

    @override
    async def get_card_copy(self, card_id: UUID, user_id: UUID) -> Card:
        stmt = (select(CardCopyModel)
                .options(joinedload(CardCopyModel.card))
                .where(CardCopyModel.card_id == card_id, CardCopyModel.copier_id == user_id))
        result = await self._session.execute(stmt)
        card_copy = result.scalars().first()
        if not card_copy:
            raise CardCopyNotFound(f'No such card copy with card_id {card_id}')
        return self.__to_entity(card_copy.card)

    @override
    async def create_card_copy(self, card_copy: CardCopy) -> CardCopy:
        try:
            card_copy_db = CardCopyModel(**card_copy.dump())
            self._session.add(card_copy_db)
            await self._session.commit()
            await self._session.refresh(card_copy_db)
            return self.__to_card_copy_entity(card_copy_db)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    def __to_entity(self, card_db: CardModel) -> Card | None:
        if not card_db:
            return None
        user_db = card_db.user
        user = self.__to_user_entity(user_db)
        author_db = card_db.author
        author = self.__to_user_entity(author_db)
        return Card(id=card_db.id,
                    card_type=card_db.card_type,
                    name=card_db.name,
                    card_type_translation=card_db.card_type_translation,
                    user_id=card_db.user_id,
                    author_id=card_db.author_id,
                    status=card_db.status,
                    order=card_db.order,
                    markdown_text=card_db.markdown_text,
                    file_id=card_db.file_id,
                    group_id=card_db.group_id,
                    created_at=card_db.created_at,
                    updated_at=card_db.updated_at,
                    result=card_db.result,
                    user=user,
                    author=author)

    def __to_sharing_url_entity(self, sharing_url_db: SharingURLModel) -> SharingURL:
        card = self.__to_entity(sharing_url_db.card)
        return SharingURL(card_id=sharing_url_db.card_id,
                          base_url=sharing_url_db.base_url,
                          code=sharing_url_db.code,
                          url=sharing_url_db.url,
                          user_id=sharing_url_db.user_id,
                          created_at=sharing_url_db.created_at,
                          updated_at=sharing_url_db.updated_at,
                          card=card)

    def __to_card_copy_entity(self, card_copy_db: CardCopyModel) -> CardCopy:
        return CardCopy(card_id=card_copy_db.card_id,
                        copier_id=card_copy_db.copier_id,
                        created_at=card_copy_db.created_at,
                        updated_at=card_copy_db.updated_at)

    def __to_user_entity(self, user_db: UserModel) -> User:
        if not user_db:
            return None
        return User(id=user_db.id,
                    first_name=user_db.first_name,
                    last_name=user_db.last_name,
                    email=user_db.email,
                    email_verified=user_db.email_verified,
                    phone_number=user_db.phone_number,
                    phone_number_verified=user_db.phone_number_verified,
                    created_at=user_db.created_at,
                    updated_at=user_db.updated_at)