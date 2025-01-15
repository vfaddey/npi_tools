from app.card_handlers.base.card_handler import CardHandler
from app.entities.card import Card
from app.repositories.card_repository import CardRepository


class CardService:
    def __init__(self,
                 repository: CardRepository,
                 handlers: list[CardHandler]):
        self._repository = repository
        self._handlers = {h.CARD_TYPE: h for h in handlers}

    async def process_card(self, card: Card) -> Card:
        ...


    async def __save_result(self, card):
        ...