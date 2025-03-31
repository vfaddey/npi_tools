from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SeamProperty:
    """
    Класс, содержащий информацию о пласте.

    :param permeability: Проницаемость пласта, м^2.
    :param volume_factor: Объёмный коэффициент, м^3/м^3.
    :param viscosity: Вязкость жидкости, сПз.
    :param thickness: Мощность пласта, м.
    :param radius_drainage: Радиус дренирования, м.
    :param xe: размер зоны дренирования прямоугольного пласта по оси Х, м.
    :param ye: размер зоны дренирования прямоугольного пласта по оси Y, м.
    :param reservoir_pressure: Начальное пластовое давление, атм.

    """

    permeability: float
    volume_factor: float
    viscosity: float
    thickness: float
    radius_drainage: float
    xe: float
    ye: float
    reservoir_pressure: float
@dataclass
class WellProperty:
    """
    Класс, содержащий информацию о скважине.

    :param rate_well: Дебит скважины, м.
    :param radius_well: Радиус скважины, м.
    :param xf: Полудлина трещины, м.
    :param permeability_fracture: Проницаемость трещины, м.
    :param width_fracture: Ширина трещины, м.
    :param array_flow_along_fracture: Массив значений притока вдоль трещины.
    :param array_accumulated_flow_in_fracture: Массив сглаженных значений притока.
    :param array_prod_coef_tail: Массив значений безразмерного коэффициента продуктивности.

    """
    rate_well: float
    radius_well: float
    xf: float
    permeability_fracture: float
    width_fracture: float
    array_flow_along_fracture: Optional[List[float]] = None
    array_accumulated_flow_in_fracture: Optional[List[float]] = None
    array_prod_coef_tail: Optional[List[float]] = None


@dataclass
class AuxiliaryProperty:
    """
    Класс, содержащий вспомогательные параметры.

    :param x_coordinate: Начальная координата, м.
    :param epsilon: Точность вычислений.
    :param accuracy: Шаг вычисления притока.
    :param k_f_tail: Проницаемость загрязненной зоны.
    :param tail_coordinate: Точка начала загрязненной зоны.
    :param array_lenght_dirt: Массив длин загрязнения.
    :param array_x_axes_smooth: Сглаженный массив координаты.

    """
    x_coordinate: float
    epsilon: float
    accuracy: float
    k_f_tail: float
    tail_coordinate: float
    array_lenght_dirt: Optional[List[float]]
    array_x_axes_smooth: Optional[List[float]] = None




