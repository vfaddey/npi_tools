import json
from aio_pika import connect, Message, DeliveryMode

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
        self.queue = None

    async def connect(self):
        self.connection = await connect(self.url)
        self.channel = await self.connection.channel()
        await self.channel.declare_queue(self.queue, durable=True)

    async def publish_card(self, card: Card):
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
            routing_key=settings.RABBITMQ_QUEUE
        )
        print(f"Published task {card.id}")

    async def close(self):
        await self.connection.close()


rabbitmq_client = RabbitMQClient(settings.RABBITMQ_URL,
                                 settings.RABBITMQ_QUEUE)
