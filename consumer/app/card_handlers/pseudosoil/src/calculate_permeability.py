import math
from typing import List
import numpy as np
from consumer.app.card_handlers.pseudosoil.src.data_class import (
    LabExperimentData,
    WellParameters,
)

# Задаем давление на выходе (атмосферное давление, Па) и первое значение давления на входе в Па
p_exit = 101325
p_vhod = 514317


def calculate_entry_pressures(
    lab_exp_data: LabExperimentData, p_exit: float, p_vhod: float
) -> List:
    """
    Функция последовательного расчета давлений на входе в образец.

    :param lab_exp_data: Объекты класса LabExperimentData.
    :param p_exit: Давление на выходе (атмосферное давление), Па.
    :param p_vhod: Первое значение давления на входе, Па.

    :return: Рассчитанные значения давлений на входе в образец.

    """

    p_vhod_values = [
        p_vhod
    ]  # В этом списке будут храниться последующие рассчитанные значения давлений на входе в образец

    for i in range(1, len(lab_exp_data.k_values)):
        p_vhod1 = (p_vhod - p_exit) * (
            lab_exp_data.flow_values[i] / lab_exp_data.flow_values[0]
        ) * lab_exp_data.k_values[i] + p_exit
        p_vhod_values.append(p_vhod1)

    return p_vhod_values


def calculate_permeability(lab_exp_data: LabExperimentData, p_vhod_values) -> List:
    """
    Функция расчета проницаемости.


    :param lab_exp_data: Объекты класса LabExperimentData.
    :param p_vhod_values: Давление на входе, Па


    :return: Рассчитанные значения проницаемости, мД

    """
    p_exit = 101325
    k_values_calculated = []

    for i in range(len(lab_exp_data.flow_values)):
        k_calculated = (
            (
                4
                * ((lab_exp_data.flow_values[i]) / 10**6)
                * (lab_exp_data.mu * 10**-3)
                * (lab_exp_data.l / 1000)
            )
            / ((np.pi * (lab_exp_data.d / 1000) ** 2) * (p_vhod_values[i] - p_exit))
        ) * 10**15
        k_values_calculated.append(k_calculated)

    return k_values_calculated


def filter_outliers(k_values_calculated, multiplier=2) -> List:
    """
    Выполняет фильтрацию выбивающихся значений в списке рассчитанных значений проницаемости.


    :param k_values_calculated: Рассчитанные значения проницаемости, мД.
    :param multiplier: Множитель для определения границ для отсечения выбивающихся значений. По умолчанию: 2.

    :return: Отфильтрованные значения проницаемости, мД.


    """
    std_k = np.std(k_values_calculated)

    # Определение границ для отсечения выбивающихся значений
    cut_off = multiplier * std_k
    lower, upper = (
        np.mean(k_values_calculated) - cut_off,
        np.mean(k_values_calculated) + cut_off,
    )

    # Фильтрация значений
    k_verified = [k for k in k_values_calculated if lower <= k <= upper]

    return k_verified


def calculate_average_permeability(k_verified) -> float:
    """
    Функция расчета среднего значения проницаемости по образцу.

    :param k_verified: Отфильтрованные значения проницаемости, мД

    :return: Среднее значение проницаемости, мД

    """
    if not k_verified:
        raise ValueError("Список отфильтрованных значений проницаемости пуст.")

    average_k = sum(k_verified) / len(k_verified)
    return average_k


def well_performance_permeability(well_param: WellParameters) -> float:
    """
    Функция расчета проницаемости по работе скважины.

    :param well_param: Объект класса WellParameters, в котором хранятся параметры скважины и режим работы.

    :return permeability: Рассчитанное значение проницаемости по работе скважины, мД

    """
    # Общее число отверстий в фильтре
    n = well_param.length_filter * well_param.perforation_density

    # Мощность пласта на одно отверстие
    thickness_per_hole = n / well_param.perforation_density

    # Площадь на одно отверстие
    area_per_hole = math.pi * well_param.well_diameter * thickness_per_hole

    # Среднее расстояние между отверстиями
    average_hole_distance = math.sqrt(area_per_hole)

    # Радиус влияния отверстий
    hole_influence_radius = (1 / 2) * average_hole_distance

    # Приток на одно отверстие в пластовых условиях
    inflow_per_hole = (
        well_param.flow_rate
        * (well_param.oil_volume_factor * 10**6)
        / (n * well_param.oil_density * 86400)
    )

    if hole_influence_radius < well_param.well_diameter:
        # Слагаемые формулы из статьи
        term1 = (hole_influence_radius - well_param.hole_radius) / (
            hole_influence_radius * well_param.hole_radius
        )
        term2 = (-0.25 / (well_param.well_diameter / 2)) * (
            math.log(hole_influence_radius / well_param.hole_radius)
        )
        term3 = (
            0.0625
            * (hole_influence_radius - well_param.hole_radius)
            / ((well_param.well_diameter / 2) ** 2)
        )
        term4 = (
            -0.0117187
            * (hole_influence_radius**2 - well_param.hole_radius**2)
            / ((well_param.well_diameter / 2) ** 3)
        )
        term5 = (
            0.0026042
            * (hole_influence_radius**3 - well_param.hole_radius**3)
            / ((well_param.well_diameter / 2) ** 4)
        )
        term6 = (
            -0.00079346
            * (hole_influence_radius**4 - well_param.hole_radius**4)
            / ((well_param.well_diameter / 2) ** 5)
        )
        term7 = (
            0.0002075
            * (hole_influence_radius**5 - well_param.hole_radius**5)
            / ((well_param.well_diameter / 2) ** 6)
        )
        term8 = (
            -0.0000610
            * (hole_influence_radius**6 - well_param.hole_radius**6)
            / ((well_param.well_diameter / 2) ** 7)
        )
        term9 = (1 / thickness_per_hole) * math.log(
            ((well_param.well_spacing * 100) / 2)
            / ((well_param.well_diameter / 2) + hole_influence_radius)
        )
        # Сумма всех слагаемых
        total_sum = (
            term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8 + term9
        )

        # Депрессия (P пл. - P заб.)
        delta_p = well_param.reservoir_pressure - well_param.bottomhole_pressure

        # Расчет проницаемости
        permeability = (
            (inflow_per_hole * well_param.reservoir_oil_viscosity)
            / (2 * math.pi * delta_p)
            * total_sum
        )

        # Перевод в мД
        permeability = permeability * 1000

        return permeability

    else:
        term1 = 1 / well_param.hole_radius
        term2 = -0.14362 * (1 / (well_param.well_diameter / 2))
        term3 = -(0.25 / (well_param.well_diameter / 2)) * math.log(
            well_param.well_diameter / well_param.hole_radius
        )
        term4 = -0.5 / hole_influence_radius
        term5 = -0.125 * (
            ((well_param.well_diameter / 2) ** 2) / hole_influence_radius**3
        )
        term6 = -0.05625 * (
            ((well_param.well_diameter / 2) ** 4) / hole_influence_radius**5
        )
        term7 = (1 / thickness_per_hole) * math.log(
            ((well_param.well_spacing * 100) / 2) + hole_influence_radius
        )
        total_sum = term1 + term2 + term3 + term4 + term5 + term6 + term7

        delta_p = well_param.reservoir_pressure - well_param.bottomhole_pressure

        # Расчет проницаемости
        permeability = (
            (inflow_per_hole * well_param.reservoir_oil_viscosity)
            / (2 * math.pi * delta_p)
            * total_sum
        )

        permeability = permeability * 1000

        return permeability
