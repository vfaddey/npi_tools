import asyncio
import json

import aio_pika
from aio_pika import IncomingMessage, Message, DeliveryMode

from app.entities.card import Card
from app.services.card_service import CardServiceFactory


class RabbitMQConsumer:
    MAX_RETRIES = 5

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
        await self.queue_object.consume(self.on_message)
        # logger.info("Started consuming messages")

    async def on_message(self, message: IncomingMessage):
        body = message.body.decode()
        data = json.loads(body)

        headers = message.headers or {}
        retries = headers.get("x-retries", 0)

        try:
            await self.__work(data)
            await message.ack()
        except Exception:
            if retries < self.MAX_RETRIES:
                new_headers = {**headers, "x-retries": retries + 1}
                await self.channel.default_exchange.publish(
                    Message(
                        message.body,
                        headers=new_headers,
                        delivery_mode=DeliveryMode.PERSISTENT,
                    ),
                    routing_key=self.queue,
                )
            # ACK оригинал в любом случае — чтобы не было зацикливания
            await message.ack()

    async def __work(self, data):
        async with self.card_service_factory.get_service() as card_service:
            await card_service.process_card(**data)

    async def close(self):
        if self.connection:
            await self.connection.close()