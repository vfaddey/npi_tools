from typing import List
from dataclasses import dataclass
import pandas as pd


@dataclass
class HydrodynamicData:
    """
    Класс, содержащий данные гидродинамических исследований и метод интерпретации.

    :param delta_t: Массив времени с начала остановки скважины, часы.
    :param delta_p: Массив изменения забойного давления с начала остановки скважины, атм.
    :param method: Список с выбранным методом интерпретации
    """

    delta_t: List[float]
    delta_p: List[float]
    method: List[str]
