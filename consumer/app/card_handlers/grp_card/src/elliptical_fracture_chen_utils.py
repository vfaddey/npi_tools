import numpy as np
from scipy.signal import wiener
from scipy.optimize import minimize_scalar
from math import cosh, sinh, asinh, tanh, cos, sin, acos, sqrt, floor, pi, log
from scipy.interpolate import interp1d
from typing import Tuple


def calc_constants(
    k_f: float, w_f: float, k: float, xf: float, mu: float, q_w: float, h: float, p_i: float, ksi_e: float, ksi_1: float
) -> Tuple[float, float, float, float, float, float]:
    """
    Функция по определению констант, необходимых для расчета по модели Chen

    Parameters
    ----------
    :param k_f: коэффициент проницаемости трещины, (м2)
    :param w_f: ширина трещины, (м)
    :param k: коэффициент проницаемости пласта, (м2)
    :param xf: полудлина трещины, (м)
    :param mu: вязкость жидкости, (Па*с)
    :param q_w: дебит скважины, (м3/с)
    :param h: мощность пласта, (м)
    :param p_i: начальное пластовое давление, (Па)
    :param ksi_e: эллиптическая координата контура питания скважины, (рад)
    :param ksi_1: эллиптическая координата трещины, (рад)

    :return: константы: f_e, c, a_1, b_0, c_3, a_1
    -------
    """
    # Раскрытость трещины на скважине
    w_f = w_f * 4 / pi
    # Безразмерная проводимость эллиптической трещины
    f_e = (k_f * w_f) / (k * xf)
    # Формула (22) из статьи Chen
    c = (2 * mu * q_w) / (pi * k * h * p_i * (sinh(2 * ksi_e) - sinh(2 * ksi_1)))
    # Формула (36) из статьи Chen
    a_1 = (-c / 8) * ((2 * sinh(2 * ksi_e) + f_e) / (f_e * cosh(2 * ksi_e) + sinh(2 * ksi_e)))
    # Формула (34) из статьи Chen
    b_0 = 1 - (c / 4) * ksi_e * sinh(2 * ksi_e) + (3 * c / 16) * cosh(2 * ksi_e) - c / 8 - a_1 / 2
    # Формула (35) из статьи Chen
    c_3 = (
        1
        - (c / 4)
        - (c / 4) * ksi_e * sinh(2 * ksi_e)
        + (3 * c / 16) * cosh(2 * ksi_e)
        + (((pi**2) * c) / (48 * f_e)) * sinh(2 * ksi_e)
        - a_1 / 2
    )
    # Формула (39) из статьи Chen
    a_1_ = a_1 / c

    return f_e, c, a_1, b_0, c_3, a_1_


def recalc_res_parameters(xf: float, w_f: float, xe: float, ye: float) -> Tuple[float, float]:
    """
    Функция перехода в эллиптическую систему координат

    Parameters
    ----------
    :param xf: полудлина трещины, (м)
    :param w_f: ширина трещины, (м)
    :param xe: размер зоны дренирования прямоугольного пласта по оси Х, (м)
    :param ye: размер зоны дренирования прямоугольного пласта по оси Y, (м)

    :return: эллиптические координаты пласта и трещины: ksi_e, ksi_1
    -------
    """
    # Пересчет параметров пласта хе, уе в эллиптические ksi_e и ksi_1
    ksi_1 = asinh((2 * w_f) / (pi * xf))

    # Прямоугольный пласт
    ksi_e = 0.5 * asinh((8 * xe * ye) / (pi * (xf**2)))
    return ksi_e, ksi_1


def calc_pwf(ksi_e: float, ksi_1: float, p_i: float, f_e: float, c: float, c_3: float, e: float) -> float:
    """
    Функция расчета забойного давления

    Parameters
    ----------
    :param ksi_e: эллиптическая координата контура питания скважины, (рад)
    :param ksi_1: эллиптическая координата трещины, (рад)
    :param p_i: начальное пластовое давление, (Па)
    :param f_e: безразмерная эллиптическая проводимость трещины
    :param c: константа C
    :param c_3: константа С3
    :param e: точность вычисления

    :return: забойное давление, (атм)
    -------
    """
    # Формула (27) из статьи Chen
    n = 2
    a_n = (c / 4) * (((-1) ** n) / n) * (sinh(2 * ksi_e) / (n * f_e * cosh(2 * n * ksi_e) + sinh(2 * n * ksi_e)))
    s_for_p_w = ((-1) ** n) * (a_n / (2 * n)) * sinh(2 * n * (ksi_e - ksi_1))
    a = s_for_p_w
    while abs(a) > e:
        n = n + 1
        if 2 * n * ksi_e > 710:
            n = n - 1
            break
        else:
            a_n = (
                (c / 4) * (((-1) ** n) / n) * (sinh(2 * ksi_e) / (n * f_e * cosh(2 * n * ksi_e) + sinh(2 * n * ksi_e)))
            )
            a = ((-1) ** n) * (a_n / (2 * n)) * sinh(2 * n * (ksi_e - ksi_1))
            s_for_p_w = s_for_p_w + a
    p_w = (-2 / f_e) * (((c * (pi**2)) / 32) * (sinh(2 * ksi_e) - sinh(2 * ksi_1)) - s_for_p_w) + c_3
    p_w = p_w * p_i / 100000
    return p_w


def calc_jd_chen(k, h, mu, ksi_e: float, f_e: float, a_1: float, e: float) -> float:
    """
    Расчет Кпрод по модели Chen

    Parameters
    ----------
    :param k: коэффиицент проницаемости пласта, (м2)
    :param h: мощность пласта, (м)
    :param mu: вязкость жидкости, (Па*с)
    :param ksi_e: эллиптическая координата контура питания скважины, (рад)
    :param f_e: безразмерная эллиптическая проводимость трещины
    :param a_1: константа A1
    :param e: точность вычисления

    :return: коэффициент продуктивности по модели Chen, (м3/(сут*МПа))
    -------
    """
    # Формулы (41-42) из статьи Chen
    n = 2
    s_for_b = (1 / (n**2)) * (1 / (1 + n * f_e * (1 / tanh(2 * n * ksi_e))))
    a = s_for_b
    while abs(a) > e:
        n = n + 1
        a = (1 / (n**2)) * (1 / (1 + n * f_e * (1 / tanh(2 * n * ksi_e))))
        s_for_b = s_for_b + a
    b_d = (
        ksi_e
        + (1 / sinh(2 * ksi_e))
        - (3 / 4) * (1 / tanh(2 * ksi_e))
        + (2 * a_1) / (sinh(2 * ksi_e))
        + (1 / f_e) * (((pi**2) / 6) + 4 * a_1 - s_for_b)
    )
    # j_pss = ((k * h * 2 * pi) / (mu * b_d)) * 86400 * 1000000
    return 1 / b_d


def calc_jd_pss_new(f_e: float, re: float, xf: float) -> float:
    """
    Функция расчета безразмерного коэффициента продуктивности

    Parameters
    ----------
    :param xf: полудлина трещины, (м)
    :param re: Радиус дренирования, м.
    :param f_e: безразмерная эллиптическая проводимость трещины

    :return: Значение безразмерного коэффициента продуктивности
    -------
    """

    u = log(f_e)
    a_1 = 0.93626800
    a_2 = -1.00489000
    a_3 = 0.31973300
    a_4 = -0.04235320
    a_5 = 0.00221799
    b_1 = -0.38553900
    b_2 = -0.06988650
    b_3 = -0.04846530
    b_4 = -0.00813558

    red = re / xf

    coef_a = a_1 + a_2 * u + a_3 * u**2 + a_4 * u**3 + a_5 * u**4
    coef_b = 1 + b_1 * u + b_2 * u**2 + b_3 * u**3 + b_4 * u**4

    bd_pss = log(red) - 0.049298 + 0.43464 * (red ** (-2)) + coef_a / coef_b

    return 1 / bd_pss


def calc_qi(
    xf: float,
    x: float,
    k: float,
    h: float,
    mu: float,
    p_i: float,
    ksi_e: float,
    ksi_1: float,
    f_e: float,
    c: float,
    accuracy: float,
    e: float,
) -> Tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    """
    Функция расчета распределения притока вдоль трещины

    Parameters
    ----------
    :param xf: полудлина трещины, (м)
    :param x: начальная координата, (м)
    :param k: коэффициент проницаемости пласта, (м2)
    :param h: мощность пласта, (м)
    :param mu: вязкость жидкости, (Па*с)
    :param p_i: начальное пластовое давление, (Па)
    :param ksi_e: эллиптическая координата контура питания скважины, (рад)
    :param ksi_1: эллиптическая координата трещины, (рад)
    :param f_e: безразмерная эллиптическая проводимость трещины
    :param c: константа C
    :param accuracy: шаг массива координаты x
    :param e: точность вычисления

    :return: рассчитанный дебит скважины, массивы притока, накопленного потока вдоль трещины и координаты
    -------
    """
    k_f = (f_e * k * xf) / 0.005

    # Формула (20) из статьи Chen
    x_start = x
    qi = np.zeros(floor((xf - x_start) / accuracy))
    qi_accum = np.zeros(floor((xf - x_start) / accuracy))
    x_axes = np.zeros(floor((xf - x_start) / accuracy))
    sum_u_x = 0
    i = 0
    while x < xf:
        # Переход от эллиптических координат
        nu = acos(x / (xf * cosh(ksi_1)))
        # Определяем сумму ряда.
        # Вычисляем первый элемент ряд при n = 2
        n = 2
        a_n = (c / 4) * (((-1) ** n) / n) * (sinh(2 * ksi_e) / (n * f_e * cosh(2 * n * ksi_e) + sinh(2 * n * ksi_e)))
        s_for_u_x = 2 * n * a_n * sinh(2 * n * (ksi_e - ksi_1)) * cos(2 * n * nu)
        a_for_u_x = s_for_u_x
        # Продолжаем суммировать до тех пор, пока элемент ряда не достигнет заданной точности, т.е. a станет < e
        while abs(a_for_u_x) > e:
            n = n + 1
            if 2 * n * ksi_e > 700:
                n = n - 1
                # print('Точность расчета для распределения притока в точке', x, ' принята ', abs(a_for_u_x))
                break
            else:
                a_n = (
                    (c / 4)
                    * (((-1) ** n) / n)
                    * (sinh(2 * ksi_e) / (n * f_e * cosh(2 * n * ksi_e) + sinh(2 * n * ksi_e)))
                )
                a_for_u_x = 2 * n * a_n * sinh(2 * n * (ksi_e - ksi_1)) * cos(2 * n * nu)
                s_for_u_x = s_for_u_x + a_for_u_x
        u_x = (
            (k / (mu * xf))
            * (p_i / (sqrt(((sinh(ksi_1)) ** 2) + ((sin(nu)) ** 2))))
            * ((c / 4) * (sinh(2 * ksi_e) - sinh(2 * ksi_1)) + s_for_u_x)
        )
        # Перевод м3/с в м3/сут:
        u_x = u_x * 86400
        # Суммарный дебит
        sum_u_x = sum_u_x + u_x
        # Заносим значения в массивы
        x_axes[i] = x
        qi[i] = u_x
        if i == 0:
            qi_accum[i] = u_x
        if i > 0:
            qi_accum[i] = qi_accum[i - 1] + u_x
        x = x + accuracy
        i = i + 1
        if i > floor((xf - x_start) / accuracy) - 1:
            break
    return (sum_u_x * 4 * accuracy * h), qi, qi_accum, x_axes


def calc_p_fracture(
    xf: float,
    x: float,
    p_i: float,
    ksi_e: float,
    ksi_1: float,
    f_e: float,
    c: float,
    c_3: float,
    accuracy: float,
    e: float,
) -> np.ndarray:
    """
    Функция расчета распределения давления вдоль трещины

    Parameters
    ----------
    :param xf: полудлина трещины, (м)
    :param x: начальная координата, (м)
    :param p_i: начальное пластовое давление, (Па)
    :param ksi_e: эллиптическая координата контура питания скважины, (рад)
    :param ksi_1: эллиптическая координата трещины, (рад)
    :param f_e: безразмерная эллиптическая проводимость трещины
    :param c: константа C
    :param c_3: константа С3
    :param accuracy: шаг массива координаты x
    :param e: точность вычисления

    :return: массив распределения давления вдоль трещины
    -------
    """
    # Формула (26) из статьи Chen
    x_start = x
    p_fi = np.zeros(floor((xf - x_start) / accuracy))
    x_axes = np.zeros(floor((xf - x_start) / accuracy))
    i = 0
    while x < xf:
        # Переход от эллиптических координат
        nu = acos(x / (xf * cosh(ksi_1)))
        # Определяем сумму ряда.
        # Вычисляем первый элемент ряд при n = 2
        n = 2
        a_n = (c / 4) * (((-1) ** n) / n) * (sinh(2 * ksi_e) / (n * f_e * cosh(2 * n * ksi_e) + sinh(2 * n * ksi_e)))
        s_for_p_f = (1 / (2 * n)) * a_n * sinh(2 * n * (ksi_e - ksi_1)) * cos(2 * n * nu)
        a = s_for_p_f
        while abs(a) > e:
            n = n + 1
            if 2 * n * ksi_e > 710:
                n = n - 1
                # print('Точность расчета для распределения давления принята ', abs(a))
                break
            else:
                a_n = (
                    (c / 4)
                    * (((-1) ** n) / n)
                    * (sinh(2 * ksi_e) / (n * f_e * cosh(2 * n * ksi_e) + sinh(2 * n * ksi_e)))
                )
                a = (1 / (2 * n)) * a_n * sinh(2 * n * (ksi_e - ksi_1)) * cos(2 * n * nu)
                s_for_p_f = s_for_p_f + a
        p_f = (-2 / f_e) * ((c / 8) * (sinh(2 * ksi_e) - sinh(2 * ksi_1)) * (nu**2) - s_for_p_f) + c_3
        p_f = p_f * p_i / 100000
        # Заносим значения в массивы
        x_axes[i] = x
        p_fi[i] = p_f
        x = x + accuracy
        i = i + 1
        if i > floor((xf - x_start) / accuracy) - 1:
            break
    return p_fi


def smoothing_qi(qi: np.ndarray, x_axes: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Функция сглаживания графика зависимости дебита от координаты

    Parameters
    ----------
    :param qi: массив распределения притока вдоль трещины, (м3/сут)
    :param x_axes: массив координаты, (м)

    :return: сглаженный массив притока, потока и координаты
    -------
    """
    x_lim = 100

    # Задаем массив значений х
    x_axes_new = np.linspace(x_axes.min(), x_axes.max(), x_lim)
    # Интерполяция значений массива qi
    qi_func = interp1d(x_axes, qi, kind='linear')
    qi_smooth = wiener(qi_func(x_axes_new))
    qi_smooth_accum = np.zeros(len(x_axes_new))
    for j in reversed(range(len(x_axes_new))):
        if j == x_lim - 1:
            qi_smooth_accum[j] = qi_smooth[j]
        if j < x_lim - 1:
            qi_smooth_accum[j] = qi_smooth[j] + qi_smooth_accum[j + 1]
    return x_axes_new, qi_smooth, qi_smooth_accum


def adaptation_alpha_q(flow: np.ndarray, x_axes: np.ndarray, xf: float) -> np.ndarray:
    """
    Функция адаптации alfa_q. Минимизирует среднеквадратичную ошибку между расчитанным притоком по Chen и Meyer

    Parameters
    ----------
    :param flow: массив значений дебитов жидкости, (м3/с)
    :param x_axes: массив значений координаты x, (м)
    :param xf: полудлина трещины, (м)

    :return: новый массив значений дебитов жидкости после минимизации среднеквадратичной ошибки между
            рассчитанным притоком по Chen и Meyer, (м3/с)
    -------
    """
    alfa_q = 1  # начальное предположение
    # alfa_q_adapt = minimize(calc_std_by_alpha_q, alfa_q, args=(flow, x_axes, xf), method='Nelder-Mead')
    alfa_q_adapt = minimize_scalar(
        calc_std_by_alpha_q, alfa_q, args=(flow, x_axes, xf), bounds=(0, 1), method='bounded'
    )
    return alfa_q_adapt.x


def calc_std_by_alpha_q(alfa_q: float, flow: np.ndarray, x_axes: np.ndarray, xf: float) -> float:
    """
    Функция расчёта среднеквадратичной ошибки между рассчитанным притоком по Chen и Meyer при заданной alpha_q

    Parameters
    ----------
    :param alfa_q: начально предполагаемое значение коэффициента альфа
    :param flow: массив значений дебитов жидкости, (м3/с)
    :param x_axes: массив значений координаты x, (м)
    :param xf: полудлина трещины, (м)

    :return: среднеквадратичная ошибка между рассчитанным притоком по Chen и Meyer при заданном alpha_q
    -------
    """
    q_calc = np.zeros(len(x_axes))
    q0 = flow[0]
    std = 0
    for i in range(0, len(x_axes)):
        x_d = x_axes[i] / xf
        q_calc[i] = q0 * (1 - x_d) ** alfa_q
        std = std + (q_calc[i] - flow[i]) ** 2
    std = std
    return std
