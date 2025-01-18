from typing import Type

from app.card_handlers.base.card_handler import CardHandler
from app.card_handlers.base.exceptions import NoSuchHandler


class HandlerManager:
    def __init__(self, *handlers: Type[CardHandler]):
        self._handlers = {
            h.CARD_TYPE: h for h in handlers
        }

    def get_handler(self, card_type: str) -> CardHandler:
        try:
            return self._handlers[card_type]()
        except KeyError:
            raise NoSuchHandler(f'No handler found for type {card_type}')
