from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.infrastructure.config import settings
from src.infrastructure.minio import init_minio
from src.infrastructure.rabbitmq.client import rabbitmq_client
from src.presentation.api.v1 import files_router, users_router, cards_router, groups_router

app = FastAPI(
    title=settings.APP_NAME
)


@app.on_event("startup")
async def startup():
    await init_minio()
    await rabbitmq_client.connect()


@app.on_event("shutdown")
async def shutdown():
    await rabbitmq_client.close()


app.include_router(files_router)
app.include_router(cards_router)
app.include_router(users_router)
app.include_router(groups_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)