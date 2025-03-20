# {"id": "72e82323-3863-43cd-95d8-bf3a04f8937b", "file_id": "cfb684be-14da-499a-8fab-71d3b0d4f189", "card_type": "pvt"}

from fastapi import FastAPI

from app.adapters.minio_client import client as minio_client
from app.adapters.rabbitmq_client import RabbitMQConsumer
from app.card_handlers.base.handler_manager import HandlerManager
from app.card_handlers.pseudosoil.pseudosoil_card import PseudosoilHandler
from app.card_handlers.simple_gdis_calculate.simple_gdis_card import SimpleGDISHandler
from app.core.config import settings
from app.db.database import AsyncSessionFactory
from app.services.card_service import CardServiceFactory

app = FastAPI()


handler_manager = HandlerManager(PseudosoilHandler,
                                 SimpleGDISHandler)
card_service_factory = CardServiceFactory(AsyncSessionFactory,
                                          minio_client,
                                          handler_manager)
consumer = RabbitMQConsumer(settings.RABBITMQ_URL,
                            settings.RABBITMQ_QUEUE,
                            card_service_factory)


@app.on_event("startup")
async def startup():
    await consumer.connect()
    await consumer.start_consuming()

@app.on_event("shutdown")
async def shutdown():
    await consumer.close()

