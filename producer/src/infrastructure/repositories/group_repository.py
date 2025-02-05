from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities import User
from src.domain.entities.card import Card
from src.domain.exceptions import GroupNotFound
from src.infrastructure.db.models.card import CardModel
from src.domain.entities.group import Group
from src.domain.repositories.group_repository import GroupRepository
from src.infrastructure.db.models import GroupModel, UserModel


class SqlaGroupRepository(GroupRepository):
    def __init__(self, session):
        self._session = session

    async def create(self, group: Group) -> Group:
        group_db = self.__from_entity(group)
        try:
            self._session.add(group_db)
            await self._session.commit()
            await self._session.refresh(group_db)
            return self.__to_entity(group_db)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def get(self, group_id: UUID) -> Group:
        stmt = select(GroupModel).where(GroupModel.id == group_id)
        result = await self._session.execute(stmt)
        group_db = result.unique().scalars().first()
        if not group_db:
            raise GroupNotFound(f'No such group with id {group_id}')
        return self.__to_entity(group_db)

    async def get_by_ids(self, group_ids: list[UUID]) -> list[Group]:
        stmt = select(GroupModel).where(GroupModel.id.in_(group_ids))
        result = await self._session.execute(stmt)
        groups_db = result.unique().scalars().all()
        return [self.__to_entity(g) for g in groups_db]

    async def get_by_user_id(self, user_id: UUID) -> list[Group]:
        stmt = select(GroupModel).where(GroupModel.user_id == user_id)
        result = await self._session.execute(stmt)
        group_db = result.unique().scalars().all()
        return [self.__to_entity(g) for g in group_db]

    async def update_name(self, group_id: UUID, group: Group) -> Group:
        try:
            group_db = await self._session.get(GroupModel, group_id)
            if not group_db:
                raise GroupNotFound(f'No such card with id {group.id}')

            # for field, value in group.dump().items():
            #     setattr(group_db, field, value)
            group_db.name = group.name

            await self._session.commit()
            await self._session.refresh(group_db)

            return self.__to_entity(group_db)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def delete(self, group_id: UUID) -> Group:
        try:
            stmt = delete(GroupModel).where(GroupModel.id == group_id).returning(GroupModel)
            result = await self._session.execute(stmt)

            await self._session.commit()
            group_db = result.scalars().first()
            if not group_db:
                raise GroupNotFound(f'No such group with id {group_id}')
            return self.__to_raw_entity(group_db)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e


    def __from_entity(self, group: Group) -> GroupModel:
        cards_db = [CardModel(**c.dump()) for c in group.cards]
        group_db = GroupModel(name=group.name,
                              user_id=group.user_id)
        group_db.cards.extend(cards_db)
        return group_db

    def __to_entity(self, group_db: GroupModel) -> Group:
        cards = [self.__to_card_entity(c) for c in group_db.cards]
        return Group(id=group_db.id,
                     user_id=group_db.user_id,
                     name=group_db.name,
                     cards=cards,
                     created_at=group_db.created_at,
                     updated_at=group_db.updated_at)

    def __to_raw_entity(self, group_db: GroupModel) -> Group:
        return Group(id=group_db.id,
                     user_id=group_db.user_id,
                     name=group_db.name,
                     cards=[],
                     created_at=group_db.created_at,
                     updated_at=group_db.updated_at)

    def __to_card_entity(self, card_db: CardModel) -> Card:
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
                    markdown_text=card_db.markdown_text,
                    file_id=card_db.file_id,
                    group_id=card_db.group_id,
                    created_at=card_db.created_at,
                    updated_at=card_db.updated_at,
                    result=card_db.result,
                    user=user,
                    author=author)


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