import json

import aio_pika
from aio_pika import IncomingMessage

from app.entities.card import Card

class RabbitMQConsumer:
    def __init__(self,
                 rabbit_url: str,
                 queue: str):
        self.rabbit_url = rabbit_url
        self.queue = queue
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
        async with message.process():
            try:
                body = message.body.decode()
                data = json.loads(body)
                card = Card(**data)
            except Exception as e:
                print(e)


    async def close(self):
        if self.connection:
            await self.connection.close()