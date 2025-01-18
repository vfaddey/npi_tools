import asyncio
import json

import aio_pika
from aio_pika import IncomingMessage

from app.entities.card import Card
from app.services.card_service import CardServiceFactory


class RabbitMQConsumer:
    def __init__(self,
                 rabbit_url: str,
                 queue: str,
                 card_service_factory: CardServiceFactory):
        self.rabbit_url = rabbit_url
        self.queue = queue
        self.card_service_factory = card_service_factory
        self.connection = None
        self.channel = None
        self.queue_object = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.rabbit_url)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=10)
            self.queue_object = await self.channel.declare_queue(self.queue, durable=True)
            # logger.info(f"Connected to RabbitMQ and declared queue '{self.queue}'")
        except Exception as e:
            # logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise e

    async def start_consuming(self):
        await self.connect()
        await self.queue_object.consume(self.on_message, no_ack=True)
        # logger.info("Started consuming messages")

    async def on_message(self, message: IncomingMessage):
        try:
            body = message.body.decode()
            data = json.loads(body)
            asyncio.create_task(self.__work(data))
        except Exception as e:
            print(e)

    async def __work(self, data):
        async with self.card_service_factory.get_service() as card_service:
            await card_service.process_card(**data)

    async def close(self):
        if self.connection:
            await self.connection.close()