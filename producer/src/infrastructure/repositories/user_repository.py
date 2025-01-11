from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import User
from src.domain.exceptions import UserNotFound

from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.db.models import UserModel


class SqlaUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: User) -> User:
        user_db = UserModel(**user.dump())
        try:
            self._session.add(user_db)
            await self._session.commit()
            await self._session.refresh(user_db)
            return User(id=user_db.id,
                        first_name=user_db.first_name,
                        last_name=user_db.last_name,
                        email=user_db.email,
                        email_verified=user_db.email_verified,
                        phone_number=user_db.phone_number,
                        phone_number_verified=user_db.phone_number_verified,
                        admin=user_db.admin,
                        created_at=user_db.created_at,
                        updated_at=user_db.updated_at)
        except SQLAlchemyError as e:
            print(e)
            await self._session.rollback()
            raise e


    async def get(self, user_id: UUID) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        user_db = result.scalars().first()
        if not user_db:
            raise UserNotFound(f'No such user with id {user_id}')
        return User(id=user_db.id,
                    first_name=user_db.first_name,
                    last_name=user_db.last_name,
                    email=user_db.email,
                    email_verified=user_db.email_verified,
                    phone_number=user_db.phone_number,
                    phone_number_verified=user_db.phone_number_verified,
                    admin=user_db.admin,
                    created_at=user_db.created_at,
                    updated_at=user_db.updated_at)

    async def update(self, user_id: UUID, user: User) -> User:
        pass

    async def delete(self, user_id: UUID):
        stmt = delete(UserModel).where(UserModel.id == user_id).returning(UserModel)

