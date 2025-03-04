from io import BytesIO
from typing import Optional
from urllib.parse import quote

from pydantic import UUID4
from starlette import status
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from src.application.exceptions.base import NPIToolsException
from src.application.exceptions.files import FileNotFound, NotAFileOwner
from src.application.use_cases.files import DeleteFileUseCase
from src.application.use_cases.get_file import GetFileUseCase, GetPublicFilesUseCase
from src.application.use_cases.get_user_files import GetUserFilesUseCase
from src.application.use_cases.upload_file import UploadFileUseCase, UploadPublicFileUseCase
from src.domain.entities import User
from src.presentation.api.deps import get_upload_file_use_case, get_current_user, get_file_use_case, \
    get_user_files_use_case, get_delete_file_use_case, get_current_admin, get_upload_public_file_use_case, \
    get_public_files_use_case
from src.presentation.schemas.file import UploadFileResponse, FileSchema

router = APIRouter(prefix='/files', tags=['files'])


@router.get('',
            response_model=list[FileSchema],
            description='Получить список всех файлов пользователя')
async def get_files(show_all: Optional[bool] = False,
                    use_case: GetUserFilesUseCase = Depends(get_user_files_use_case),
                    user: User = Depends(get_current_user)):
    return await use_case.execute(user.id, show_all)


@router.post('/upload',
             status_code=status.HTTP_201_CREATED,
             response_model=UploadFileResponse,
             description='Загрузка файла')
async def upload_file(uploaded_file: UploadFile,
                      use_case: UploadFileUseCase = Depends(get_upload_file_use_case),
                      user: User = Depends(get_current_user)):
    try:
        file_data = await uploaded_file.read()
        file = await use_case.execute(user.id, file_data, uploaded_file.filename)
        return UploadFileResponse(id=file.id)
    except NPIToolsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/public',
            response_model=list[FileSchema],
            description='Список публичных файлов')
async def get_public_files(use_case: GetPublicFilesUseCase = Depends(get_public_files_use_case)):
    try:
        result = await use_case.execute()
        return result
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/{file_id}',
            description='Скачать файл по id')
async def get_file_by_id(file_id: UUID4,
                         use_case: GetFileUseCase = Depends(get_file_use_case),
                         user: User = Depends(get_current_user),
                         ):
    try:
        file, data = await use_case.execute(file_id, user.id)
        encoded_filename = quote(file.filename)
        if file.filename.endswith('.svg'):
            return StreamingResponse(
                BytesIO(data),
                media_type='image/svg+xml',
            )
        if file.filename.endswith('.png'):
            return StreamingResponse(
                BytesIO(data),
                media_type='image/png',
            )
        return StreamingResponse(
            BytesIO(data),
            media_type='application/octet-stream',
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )
    except FileNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NotAFileOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete('/{file_id}',
               response_model=UploadFileResponse,
               description='Удалить файл по ID')
async def delete_file(file_id: UUID4,
                      user: User = Depends(get_current_user),
                      use_case: DeleteFileUseCase = Depends(get_delete_file_use_case)):
    try:
        result = await use_case.execute(file_id, user.id)
        return result
    except NotAFileOwner as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except FileNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post('/upload/public',
             description='Загрузить публичный файл с описанием')
async def upload_public_file(uploaded_file: UploadFile,
                             description: Optional[str],
                             use_case: UploadPublicFileUseCase = Depends(get_upload_public_file_use_case),
                             admin: User = Depends(get_current_admin)):
    try:
        file_data = await uploaded_file.read()
        file = await use_case.execute(admin.id, file_data, uploaded_file.filename, description)
        return UploadFileResponse(id=file.id)
    except NPIToolsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
