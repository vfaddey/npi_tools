import asyncio
from minio import Minio
from minio.error import S3Error
from src.infrastructure.config import settings

client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

BUCKET_NAME = settings.MINIO_BUCKET_NAME

async def ensure_bucket_exists():
    loop = asyncio.get_event_loop()
    exists = await loop.run_in_executor(None, client.bucket_exists, BUCKET_NAME)
    if not exists:
        await loop.run_in_executor(None, client.make_bucket, settings.MINIO_BUCKET_NAME)
    else:
        print(f"Bucket '{BUCKET_NAME}' уже существует.")

async def init_minio():
    await ensure_bucket_exists()


