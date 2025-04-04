from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from starlette import status

from src.application.exceptions.base import NPIToolsException
from src.application.exceptions.cards import NotACardOwner, SharingError, FailedToDeleteCard
from src.application.exceptions.files import NotAFileOwner, FileNotFound
from src.application.exceptions.groups import NotAGroupOwner
from src.application.use_cases.cards import CreateCardUseCase, GetUserCardsUseCase, GetCardUseCase, DeleteCardUseCase, \
    UpdateCardUseCase, MoveCardUseCase, CalculateCardUseCase, CreateShareURlUseCase, CopyBySharingCodeUseCase
from src.domain.entities import User, Card
from src.domain.entities.card import CardType, CARD_TYPE_TRANSLATIONS
from src.domain.exceptions import GroupNotFound
from src.domain.exceptions.cards import CardNotFound, SharingUrlNotFound
from src.presentation.api.deps import get_current_user, get_create_card_use_case, get_card_use_case, \
    get_delete_card_use_case, get_user_cards_use_case, get_update_card_use_case, get_move_card_use_case, \
    get_calculate_card_use_case, get_create_sharing_url_use_case, get_copy_by_sharing_code_use_case
from src.presentation.schemas.card import CreateCardSchema, CardSchema, \
    UpdateCardSchema, CreateShareUrlSchema, MoveCardSchema, ShareUrlSchema

router = APIRouter(prefix="/cards", tags=["cards"])


@router.post('',
             response_model=CardSchema,
             status_code=status.HTTP_201_CREATED,
             description='Создать карточку')
async def create_card(card: CreateCardSchema,
                      use_case: CreateCardUseCase = Depends(get_create_card_use_case),
                      user: User = Depends(get_current_user)):
    try:
        result = await use_case.execute(Card(**card.model_dump()), user.id)
        response = CardSchema(**result.dump())
        return response
    except (NotAFileOwner, NotACardOwner) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FileNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get('/types',
            description='Список всех доступных карточек')
async def get_types():
    return [
        {
        'type': t,
        'translation': CARD_TYPE_TRANSLATIONS.get(t)
        }
        for t in CardType
    ]


@router.get('',
            response_model=list[CardSchema],
            description='Список карточек пользователя')
async def list_cards(user: User = Depends(get_current_user),
                     use_case: GetUserCardsUseCase = Depends(get_user_cards_use_case)):
    try:
        return await use_case.execute(user.id)
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post('/calculate/{card_id}',
             response_model=CardSchema,
             description='Создать задачу на расчет карточки')
async def calculate_card(card_id: UUID4,
                         user: User = Depends(get_current_user),
                         use_case: CalculateCardUseCase = Depends(get_calculate_card_use_case)):
    try:
        result = await use_case.execute(card_id, user.id)
        return CardSchema(**result.dump())
    except NotACardOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except (CardNotFound, FileNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch('',
              response_model=CardSchema,
              description='Обновить карточку')
async def update_card(card: UpdateCardSchema,
                      user: User = Depends(get_current_user),
                      use_case: UpdateCardUseCase = Depends(get_update_card_use_case)):
    try:
        result = await use_case.execute(Card(**card.model_dump()), user.id)
        return CardSchema(**result.dump())
    except (CardNotFound, FileNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NotACardOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put('',
            response_model=CardSchema,
            description='Переместить карточку в другую группу')
async def move_card(schema: MoveCardSchema,
                    user: User = Depends(get_current_user),
                    use_case: MoveCardUseCase = Depends(get_move_card_use_case)):
    try:
        updated = await use_case.execute(schema.card_id, schema.group_id, schema.order, user.id)
        return CardSchema(**updated.dump())
    except CardNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NotACardOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NotAGroupOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except GroupNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



@router.delete('/{card_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               description='Удаление карточки')
async def delete_card(card_id: UUID4,
                      user: User = Depends(get_current_user),
                      use_case: DeleteCardUseCase = Depends(get_delete_card_use_case)):
    try:
         return await use_case.execute(card_id, user.id)
    except CardNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NotACardOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except FailedToDeleteCard as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post('/share',
             status_code=status.HTTP_201_CREATED,
             response_model=ShareUrlSchema,
             description='Сгенерировать ссылку на шэринг карточки, используя url фронта')
async def create_share_url(schema: CreateShareUrlSchema,
                           user: User = Depends(get_current_user),
                           use_case: CreateShareURlUseCase = Depends(get_create_sharing_url_use_case)):
    try:
        result = await use_case.execute(schema.card_id, str(schema.base_url), user.id)
        return ShareUrlSchema(**result.dump())
    except CardNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NotACardOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/share',
            response_model=CardSchema,
            description='Получить карточку по коду шэринга. Карточка копируется в список карточек')
async def get_card_by_sharing_code(code: str,
                                   user: User = Depends(get_current_user),
                                   use_case: CopyBySharingCodeUseCase = Depends(get_copy_by_sharing_code_use_case)):
    try:
        result = await use_case.execute(code, user.id)
        return CardSchema(**result.dump())
    except SharingError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FileNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CardNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SharingUrlNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



@router.get('/{card_id}',
            response_model=CardSchema,
            description='Информация по отдельной карточке')
async def get_card(card_id: UUID4,
                   user: User = Depends(get_current_user),
                   use_case: GetCardUseCase = Depends(get_card_use_case)):
    try:
        return await use_case.execute(card_id, user.id)
    except CardNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NotACardOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))