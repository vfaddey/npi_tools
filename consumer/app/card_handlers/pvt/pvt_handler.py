from consumer.app.card_handlers.base.card_handler import CardHandler, HandlerResult, DataAsset
import pandas as pd

from producer.src.domain.entities.task import CardType


class PVTHandler(CardHandler):
    CARD_TYPE = CardType.PVT

    def process(self, data) -> HandlerResult:

        img1 = None
        img2 = None
        as1 = DataAsset('graph', '.png', img1)
        as2 = DataAsset('graph', '.png', img2)
        js = {
            'sq': [1, 2, 3, 4, 5]
        }
        result = HandlerResult(
            data=js,
            assets=[as1, as2],
        )
        return result

    def validate(self, data):
        if not data:
            raise Exception('No data provided')


handler = PVTHandler()

