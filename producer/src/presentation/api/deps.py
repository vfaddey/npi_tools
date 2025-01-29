from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.exceptions.user import FailedToAuthorize
from src.application.services.card_service import CardService
from src.application.services.group_service import GroupService

from src.application.services.user_service import UserService
from src.application.use_cases.cards import CreateCardUseCase, GetCardUseCase, UpdateCardUseCase, DeleteCardUseCase, \
    GetUserCardsUseCase, MoveCardUseCase, CalculateCardUseCase
from src.application.use_cases.files import DeleteFileUseCase
from src.application.use_cases.get_file import GetFileUseCase, GetPublicFilesUseCase
from src.application.use_cases.get_user import GetUserUseCase
from src.application.use_cases.get_user_files import GetUserFilesUseCase
from src.application.use_cases.groups import GetGroupsUseCase, RenameGroupUseCase, DeleteGroupUseCase, \
    CreateGroupUseCase
from src.domain.adapters import AuthAdapter
from src.domain.entities import User
from src.domain.exceptions import UserNotFound
from src.domain.repositories.group_repository import GroupRepository
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.config import settings
from src.infrastructure.rabbitmq.client import rabbitmq_client
from src.infrastructure.repositories.card_repository import SqlaCardRepository
from src.infrastructure.adapters import NPIAuthAdapter
from src.application.services.file_service import FileService
from src.application.use_cases.upload_file import UploadFileUseCase, UploadPublicFileUseCase
from src.infrastructure.db.database import AsyncSessionFactory
from src.infrastructure.minio import client as minio_client
from src.infrastructure.repositories.file_repository import SqlaFileRepository
from src.infrastructure.repositories.group_repository import SqlaGroupRepository
from src.infrastructure.repositories.user_repository import SqlaUserRepository

http_bearer = HTTPBearer()


async def get_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_file_repository(session: AsyncSession = Depends(get_session)) -> SqlaFileRepository:
    return SqlaFileRepository(session)

async def get_card_repository(session: AsyncSession = Depends(get_session)) -> SqlaCardRepository:
    return SqlaCardRepository(session)

async def get_user_repository(session: AsyncSession = Depends(get_session)) -> SqlaUserRepository:
    return SqlaUserRepository(session)

async def get_group_repository(session: AsyncSession = Depends(get_session)) -> GroupRepository:
    return SqlaGroupRepository(session)




async def get_file_service(file_repo: SqlaFileRepository = Depends(get_file_repository)) -> FileService:
    return FileService(file_repo,
                       minio_client)

async def get_upload_file_use_case(file_service: FileService = Depends(get_file_service)) -> UploadFileUseCase:
    return UploadFileUseCase(file_service)

async def get_upload_public_file_use_case(file_service: FileService = Depends(get_file_service)) -> UploadPublicFileUseCase:
    return UploadPublicFileUseCase(file_service)

async def get_public_files_use_case(file_service: FileService = Depends(get_file_service)) -> GetPublicFilesUseCase:
    return GetPublicFilesUseCase(file_service)

async def get_file_use_case(file_service: FileService = Depends(get_file_service)) -> GetFileUseCase:
    return GetFileUseCase(file_service)

async def get_user_files_use_case(file_service: FileService = Depends(get_file_service)):
    return GetUserFilesUseCase(file_service)

async def get_delete_file_use_case(file_service: FileService = Depends(get_file_service)):
    return DeleteFileUseCase(file_service)

async def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)

async def get_auth_adapter():
    return NPIAuthAdapter(settings.AUTH_SERVER_URL,
                          settings.USERINFO_URI)

async def get_user_use_case(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                            user_service: UserService = Depends(get_user_service),
                            auth_adapter: AuthAdapter = Depends(get_auth_adapter)) -> GetUserUseCase:
    token = credentials.credentials
    return GetUserUseCase(user_service,
                          auth_adapter,
                          token)



async def get_group_service(group_repository: GroupRepository = Depends(get_group_repository)) -> GroupService:
    return GroupService(group_repository)


async def get_groups_use_case(group_service: GroupService = Depends(get_group_service)) -> GetGroupsUseCase:
    return GetGroupsUseCase(group_service)


async def get_rename_group_use_case(group_service: GroupService = Depends(get_group_service)) -> RenameGroupUseCase:
    return RenameGroupUseCase(group_service)

async def get_delete_group_use_case(group_service: GroupService = Depends(get_group_service)) -> DeleteGroupUseCase:
    return DeleteGroupUseCase(group_service)

async def get_create_group_use_case(group_service: GroupService = Depends(get_group_service)) -> CreateGroupUseCase:
    return CreateGroupUseCase(group_service)


async def get_card_service(card_repository: SqlaCardRepository = Depends(get_card_repository)) -> CardService:
    return CardService(card_repository, rabbitmq_client)

async def get_card_use_case(card_service: CardService = Depends(get_card_service),
                            user_service: UserService = Depends(get_user_service)):
    return GetCardUseCase(card_service, user_service)

async def get_user_cards_use_case(card_service: CardService = Depends(get_card_service)) -> GetUserCardsUseCase:
    return GetUserCardsUseCase(card_service)

async def get_update_card_use_case(card_service: CardService = Depends(get_card_service),
                                   file_service: FileService = Depends(get_file_service)):
    return UpdateCardUseCase(card_service, file_service)

async def get_calculate_card_use_case(card_service: CardService = Depends(get_card_service)) -> CalculateCardUseCase:
    return CalculateCardUseCase(card_service)

async def get_move_card_use_case(card_service: CardService = Depends(get_card_service),
                                 group_service: GroupService = Depends(get_group_service)) -> MoveCardUseCase:
    return MoveCardUseCase(card_service, group_service)

async def get_delete_card_use_case(card_service: CardService = Depends(get_card_service),
                                   user_service: UserService = Depends(get_user_service)):
    return DeleteCardUseCase(card_service, user_service)



async def get_create_card_use_case(card_service: CardService = Depends(get_card_service),
                                   file_service: FileService = Depends(get_file_service),
                                   group_service: GroupService = Depends(get_group_service)) -> CreateCardUseCase:
    return CreateCardUseCase(card_service,
                             file_service,
                             group_service)



async def get_current_user(use_case: GetUserUseCase = Depends(get_user_use_case)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        return await use_case.execute()
    except FailedToAuthorize as e:
        raise credentials_exception
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

async def get_current_admin(user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to perform this action")
    return user

