from pathlib import Path
from typing import Tuple
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d
from consumer.app.card_handlers.pseudosoil.src.excel_reader import (
    read_parameters_isotropic,
    get_selected_case,
)


def calculate_case_1(parameters) -> Tuple[float, float, float]:
    """
    Функция расчета пористости, проницаемости и удельной поверхности в случае одинаковых капилляров.

    :param parameters: Кортеж параметров, содержащий r0, n, d.

    :return: Значения пористости, проницаемости и удельной поверхности.
    """
    r0, n, d, selected_case = parameters
    # Расчет пористости
    phi_result = np.pi * (r0**2) * n * 10**-2

    # Расчет проницаемости
    k_result = (np.pi / 8) * n * (r0**4) * 10**7

    # Расчет удельной поверхности
    S_result = 6 * (1 - (phi_result / 100)) / (d * 10**-3)

    return phi_result, k_result, S_result


file_path = Path("Входной файл.xlsx")
selected_case = get_selected_case(file_path)


if selected_case == "Одинаковые капилляры":
    # Получаем параметры в зависимости от выбранного случая
    parameters = read_parameters_isotropic(file_path)
    # Расчет в зависимости от выбранного случая
    result = calculate_case_1(parameters)
    phi, k, S = result
    phi = round(phi, 3)
    k = round(k, 3)
    S = round(S, 1)
    print(f"Пористость: {phi} д.ед")
    print(f"Проницаемость: {k} мД")
    print(f"Удельная поверхность: {S} м^2/м^3")


def integrand_k(r, rho_interp_func) -> float:
    """
    Функция возвращения значения подынтегральной функции для расчета проницаемости.

    :param r: Радиус капилляра, мм
    :param rho_interp_func: Функция распределения

    :return: Значение подынтегральной функции для расчета проницаемости.
    """
    return np.pi * r**4 * rho_interp_func(r)


def integrand_phi(r, rho_interp_func) -> float:
    """
    Функция возвращения значений подынтегральной функции для расчета пористости.

    :param r: Радиус капилляра, мм
    :param rho_interp_func: Функция распределения

    :return: Значение подынтегральной функции для расчета пористости.
    """
    return np.pi * r**2 * rho_interp_func(r)


def calculate_specific_surface_area(result_phi, d) -> float:
    """
    Функция для расчета удельной поверхности

    :param result_phi: Пористость, д.ед.
    :param d: Диаметр частиц (фракции), мм

    :return: Значение удельной поверхности, м^2/м^3
    """

    S: float = 6 * (1 - result_phi) / (d * 10**-3)
    return S


def integrand_k_uneven(r, rho_interp_func) -> float:
    """
    Функция возвращения значения подынтегральной функции для расчета проницаемости при неравномерном распределении

    :param r: Радиус капилляра, мм
    :param rho_interp_func: Функция распределения

    :return: Значение подынтегральной функции для расчета проницаемости.
    """
    return np.pi * r**4 * rho_interp_func(r)


def integrand_phi_uneven(r, rho_interp_func) -> float:
    """
    Функция возвращения значения подынтегральной функции для расчета пористости при неравномерном распределении

    :param r: Радиус капилляра, мм
    :param rho_interp_func: Функция распределения

    :return: Значение подынтегральной функции для расчета пористости.
    """
    return np.pi * r**2 * rho_interp_func(r)


def calculate_specific_surface_area_uneven(result_phi, d) -> float:
    """
    Функция для расчета удельной поверхности при неравномерном случае

    :param result_phi: Пористость, д.ед.
    :param d: Диаметр частиц (фракции), мм

    :return: Значение удельной поверхности, м^2/м^3
    """
    S: float = 6 * (1 - result_phi) / (d * 10**-3)
    return S


def calculate_case_2(parameters) -> Tuple[float, float, float]:
    """
    Функция для расчета случая "Капилляры с равномерным распределением"

    :param parameters: Кортеж параметров, содержащий rmin, rmax, n, d, x1, y1, x2, y2, x3, y3.

    :return: Проницаемость, пористость, удельная поверхность
    """
    # Распаковка параметров
    rmin, rmax, n, d, x1, y1, x2, y2, x3, y3, selected_case = parameters

    # Преобразование единиц измерения
    rmax = rmax * 10**-3
    rmin = rmin * 10**-3
    n = n * 10**4

    # Преобразование координат точек
    points_rho = [(x * 10**-3, y * 10**3) for x, y in [(x1, y1), (x2, y2), (x3, y3)]]
    r_points, rho_points = zip(*points_rho)

    # Интерполяция
    rho_interp_func = interp1d(
        r_points, rho_points, kind="linear", fill_value="extrapolate"
    )

    # Определение границы интегрирования
    lower_limit = rmin
    upper_limit = rmax

    # Вычисление интегралов
    result_k, error = quad(
        lambda r: (n / 8) * integrand_k(r, rho_interp_func), lower_limit, upper_limit
    )
    result_phi, error_phi = quad(
        lambda r: n * integrand_phi(r, rho_interp_func), lower_limit, upper_limit
    )

    # Округление результатов
    result_phi = round(result_phi, 3)
    result_k = round(result_k * 10**15, 3)

    # Вычисление удельной поверхности
    specific_surface_area = calculate_specific_surface_area(result_phi, d)
    specific_surface_area = round(specific_surface_area, 1)

    return result_k, result_phi, specific_surface_area


# Проверка выбранного случая
if selected_case == "Капилляры с равномерным распределением":
    # Получаем параметры в зависимости от выбранного случая
    parameters = read_parameters_isotropic(file_path)
    # Вычисление результатов и вывод
    result_k, result_phi, specific_surface_area = calculate_case_2(parameters)
    print(f"Пористость: {result_phi} д.ед")
    print(f"Проницаемость: {result_k} мД")
    print(f"Удельная поверхность: {specific_surface_area} м^2/м^3")


def calculate_case_3(parameters) -> Tuple[float, float, float]:
    """
    Функция для расчета случая "Капилляры с неравномерным распределением"

    :param parameters: Кортеж параметров, содержащий rmin, rmax, n, d, x1, y1, x2, y2, x3, y3.

    :return: Проницаемость, пористость, удельная поверхность
    """
    rmin, rmax, n, d, x1, y1, x2, y2, x3, y3, selected_case = parameters
    rmax = rmax * 10**-3
    rmin = rmin * 10**-3
    n = n * 10**4

    # Преобразование координат точек
    points_rho = [(x * 10**-3, y * 10**3) for x, y in [(x1, y1), (x2, y2), (x3, y3)]]
    r_points, rho_points = zip(*points_rho)

    # Интерполяция
    rho_interp_func = interp1d(
        r_points, rho_points, kind="linear", fill_value="extrapolate"
    )

    # Определение границы интегрирования
    lower_limit = rmin
    upper_limit = rmax

    # Вычисление интегралов
    result_k, error = quad(
        lambda r: (n / 8) * integrand_k(r, rho_interp_func), lower_limit, upper_limit
    )
    result_phi, error_phi = quad(
        lambda r: n * integrand_phi(r, rho_interp_func), lower_limit, upper_limit
    )

    # Округление результатов
    result_phi = round(result_phi, 3)
    result_k = round(result_k * 10**15, 3)

    # Вычисление удельной поверхности
    specific_surface_area = calculate_specific_surface_area(result_phi, d)
    specific_surface_area = round(specific_surface_area, 1)

    return result_k, result_phi, specific_surface_area


if selected_case == "Капилляры с неравномерным распределением":
    # Получаем параметры в зависимости от выбранного случая
    parameters = read_parameters_isotropic(file_path)
    # Вычисление результатов и вывод
    result_k, result_phi, specific_surface_area = calculate_case_3(parameters)
    print(f"Пористость: {result_phi} д.ед")
    print(f"Проницаемость: {result_k} мД")
    print(f"Удельная поверхность: {specific_surface_area} м^2/м^3")


def calculate_case_4(parameters) -> Tuple[float, float]:
    """
    Функция для расчета случая "Одинаковые трещины"

    :param parameters: Кортеж параметров, содержащий w (раскрытость трещин), xi (плотность трещин на метр)

    :return: Проницаемость, пористость
    """
    w, xi, selected_case = parameters
    k_4 = (((w * 10**-3) ** 3 / 12) * xi) * 10**15
    phi_4 = (w * 10**-3) * xi * 100
    return k_4, phi_4


if selected_case == "Одинаковые трещины":
    # Получаем параметры в зависимости от выбранного случая
    parameters = read_parameters_isotropic(file_path)
    result_4 = calculate_case_4(parameters)
    k_4, phi_4 = result_4
    print(f"Пористость: {phi_4} %")
    print(f"Проницаемость: {round(k_4, 3)} мД")


def integrand_k_w(w, rho_interp_func) -> float:
    """
    Функция возвращения значения подынтегральной функции для расчета проницаемости в случае трещин.

    :param w: Раскрытие трещины, мм
    :param rho_interp_func: Функция распределения

    :return: Значение подынтегральной функции для расчета проницаемости в случае трещин.
    """
    return ((w**3) / 12) * rho_interp_func(w)


def integrand_phi_w(w, rho_interp_func) -> float:
    """
    Функция возвращения значения подынтегральной функции для расчета пористости в случае трещин.

    :param w: Раскрытие трещины, мм
    :param rho_interp_func: Функция распределения

    :return: Значение подынтегральной функции для расчета пористости в случае трещин.
    """
    return w * rho_interp_func(w)


def calculate_case_5(parameters) -> Tuple[float, float]:
    """
    Функция для расчета случая "Трещины с равномерным распределением"

    :param parameters: Кортеж параметров, содержащий wmin, wmax, xi, x1, y1, x2, y2, x3, y3.

    :return: Проницаемость, пористость
    """
    wmin, wmax, xi, x1, y1, x2, y2, x3, y3, selected_case = parameters
    w_min = wmin * 10**-3
    w_max = wmax * 10**-3
    points_rho = [(x * 10**-3, y * 10**3) for x, y in [(x1, y1), (x2, y2), (x3, y3)]]
    w_points, rho_points = zip(*points_rho)
    rho_interp_func = interp1d(
        w_points, rho_points, kind="linear", fill_value="extrapolate"
    )
    lower_limit = w_min
    upper_limit = w_max
    result_k, error_k = quad(
        lambda w: xi * integrand_k_w(w, rho_interp_func), lower_limit, upper_limit
    )
    result_phi, error_phi = quad(
        lambda w: xi * integrand_phi_w(w, rho_interp_func), lower_limit, upper_limit
    )
    result_phi = result_phi * 100
    k = result_k * 10**15
    return k, result_phi


if selected_case == "Трещины с равномерным распределением":
    # Получаем параметры в зависимости от выбранного случая
    parameters = read_parameters_isotropic(file_path)
    k, result_phi = calculate_case_5(parameters)
    print(f"Пористость: {round(result_phi, 4)} %")
    print(f"Проницаемость: {round(k, 3)} мД")


def calculate_case_6(parameters) -> Tuple[float, float]:
    """
    Функция для расчета случая "Трещины с неравномерным распределением"

    :param parameters: Кортеж параметров, содержащий wmin, wmax, xi, x1, y1, x2, y2, x3, y3.

    :return: Проницаемость, пористость
    """
    wmin, wmax, xi, x1, y1, x2, y2, x3, y3, selected_case = parameters
    w_min = wmin * 10**-3
    w_max = wmax * 10**-3
    points_rho = [(x * 10**-3, y * 10**3) for x, y in [(x1, y1), (x2, y2), (x3, y3)]]
    w_points, rho_points = zip(*points_rho)
    rho_interp_func = interp1d(
        w_points, rho_points, kind="linear", fill_value="extrapolate"
    )
    lower_limit = w_min
    upper_limit = w_max
    result_k, error_k = quad(
        lambda w: xi * integrand_k_w(w, rho_interp_func), lower_limit, upper_limit
    )
    result_phi, error_phi = quad(
        lambda w: xi * integrand_phi_w(w, rho_interp_func), lower_limit, upper_limit
    )
    result_phi = result_phi * 100
    k = result_k * 10**15
    return k, result_phi


if selected_case == "Трещины с неравномерным распределением":
    # Получаем параметры в зависимости от выбранного случая
    parameters = read_parameters_isotropic(file_path)
    k, result_phi = calculate_case_5(parameters)
    print(f"Пористость: {round(result_phi, 4)} %")
    print(f"Проницаемость: {round(k, 3)} мД")


def calculate_case_7(parameters) -> float:
    """
    Функция расчета радиуса поры через пористость и проницаемость.

    :param parameters: Кортеж считанных значений пористости и проницаемости

    :return: Радиус поры, мм
    """
    k, phi, selected_case = parameters
    r0 = (np.sqrt((8 * k * 10**-15) / phi)) * 10**3
    rounded_r0 = round(r0, 4)
    return rounded_r0


if selected_case == "Расчет радиуса поры":
    # Получаем параметры в зависимости от выбранного случая
    parameters = read_parameters_isotropic(file_path)
    resulting_r0 = calculate_case_7(parameters)
    # Выводим полученное значение радиуса поры
    print(f"Радиус поры (r0): {resulting_r0} мм")
