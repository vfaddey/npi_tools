from abc import ABC, abstractmethod


from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DataAsset:
    asset_type: str # пример: table, graph
    file_format: str # пример: .png, .csv, .xslx итд
    data: Any # файл непосредственно

@dataclass
class HandlerResult:
    data: Optional[dict[str, Any]] # json с результатами
    assets: Optional[list[DataAsset]] # массив файлов


class CardHandler(ABC):
    CARD_TYPE: str = 'base'

    @abstractmethod
    def process(self, data) -> HandlerResult:
        raise NotImplementedError

    @abstractmethod
    def validate(self, data):
        raise NotImplementedError

