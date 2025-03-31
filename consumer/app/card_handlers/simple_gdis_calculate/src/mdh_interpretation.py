import math
from typing import List
import typing as tp
from math import log10
from app.card_handlers.simple_gdis_calculate.src.Hydrodynamic_Data import (
    HydrodynamicData,
)
import numpy as np
from app.card_handlers.simple_gdis_calculate.src.Fluid_info import FormationInfo


def calculate_lg_t(hydrodynamic_data: HydrodynamicData) -> List[float]:
    """
    Функция вычисления десятичного логарифма от значений массива delta_t.

    :param hydrodynamic_data: Объект класса HydrodynamicData с данными гидродинамических исследований.
    :return: Массив значений десятичного логарифма от delta_t.
    """
    delta_t_values = hydrodynamic_data.delta_t
    lg_t_values = [log10(value * 3600) for value in delta_t_values]
    return lg_t_values


# lg_t_result = calculate_lg_t(hydrodynamic_data)
# delta_p = hydrodynamic_data.delta_p


# print(delta_p)
# print("Результаты расчета lg(t):", lg_t_result)


def calculate_mdh(
    formation_info: FormationInfo, inter_segment: float, coef_angle_incl: float
) -> tp.Tuple[float, float, float, float, tp.Union[float, int]]:
    """
    Функция вычисления основных параметров по методу MDH.

    :param formation_info: Объект класса FormationInfo с данными о пласте и флюиде.
    :param inter_segment:
    :param coef_angle_incl:

    :return: Кортеж из пяти значений: epsilon, param, piezo, K_prod, k.
    """

    Q_0 = formation_info.Q
    b = formation_info.b
    density = formation_info.density
    h = formation_info.h
    mu = formation_info.mu
    c_total = formation_info.c_total
    distance = formation_info.distance
    epsilon = (2.3 * Q_0 * 11.57 * b) / (4 * np.pi * coef_angle_incl * density)
    param = (10 ** (inter_segment / coef_angle_incl)) / 2.25
    piezo = epsilon / ((h * 100) * c_total)
    r_pr = math.sqrt(piezo / param)
    K = (2 * np.pi * epsilon) / (2.3 * log10(((distance * 100) / 2) / r_pr))
    K_prod = (K * density) / (11.57 * b)
    k = (epsilon * mu) / (h * 100) * 10**3

    return (
        round(epsilon, 3),
        round(param, 3),
        round(piezo, 3),
        round(K_prod, 3),
        round(k, 3),
    )
