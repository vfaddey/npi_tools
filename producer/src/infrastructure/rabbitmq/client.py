import json

import aio_pika
from aio_pika import Message, DeliveryMode

from src.domain.entities import Card
from src.infrastructure.config import settings

class RabbitMQClient:
    def __init__(self,
                 url,
                 queue):
        self.url = url
        self.queue = queue
        self.connection = None
        self.channel = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=10)
            queue_object = await self.channel.declare_queue(self.queue, durable=True)
        except Exception as e:
            raise e

    async def publish_card(self, card: Card):
        try:
            data = {
                'id': str(card.id),
                'file_id': str(card.file_id),
                'card_type': card.card_type,
            }
            message = Message(
                json.dumps(data).encode(),
                delivery_mode=DeliveryMode.PERSISTENT
            )
            await self.channel.default_exchange.publish(
                message,
                routing_key=self.queue
            )
            print(f"Published task {card.id}")
        except Exception as e:
            print(f"Error publishing task {card.id}: {e}")

    async def close(self):
        await self.connection.close()


rabbitmq_client = RabbitMQClient(settings.RABBITMQ_URL,
                                 settings.RABBITMQ_QUEUE)
