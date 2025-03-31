from math import sqrt, pi, exp, log
from scipy.interpolate import interp1d
import numpy as np


def calc_j_d_finite_tail_in(
    lambd: float,
    sigma_inf: float,
    sigma_w: float,
    re: float,
    alpha_q: float,
    wf: float,
    k: float,
    c_a: float,
    k_f1: float,
    k_f2: float,
    sigma_bound: float,
    ix: float,
    xf: float,
) -> float:
    """
    Функция расчета безразмерного коэффициента продуктивности по методике Meyer для вертикальной трещины постоянной
    конечной проводимости с загрязнением на конце.
    (см. формулы (39) - (42))
    J_D for Uniform Finite-Variable-Conductivity Fracture, Tail-in model

    Parameters
    ----------
    :param lambd: соотношение сторон пласта, безразм.
    :param sigma_inf:
    :param sigma_w:
    :param re: Радиус зоны дренирования, м
    :param alpha_q: коэффициент мощности потока в трещине, безразм.
    :param wf: Ширина трещины, м
    :param k: Проницаемость пласта, м^2
    :param c_a: форм-фактор, безразм.
    :param k_f1: Проницаемость незгрязненного участка трещины, м^2
    :param k_f2: Проницаемость згрязненного участка трещины, м^2
    :param sigma_bound:
    :param ix: Коэффициент проникновения, безразм.
    :param xf: Длина трещины, м

    :return: безразмерный коэффициент продуктивности
    -------
    """

    beta_re = sqrt(4 * pi / (exp(0.5772156649) * c_a))
    g_inf = 2 * lambd / (1 + 1 / lambd)
    g_0 = 2 / (1 + 1 / lambd)

    # первая часть трещины
    c_fd1 = wf * (k_f1 / k - 1) / xf
    phi1 = exp(-2 * c_fd1 * ix**2)
    g1 = phi1 * g_0 + (1 - phi1) * g_inf
    c1 = c_fd1 * g1 * sigma_inf / (2 * pi)

    # вторая часть трещины
    c_fd2 = wf * (k_f2 / k - 1) / xf
    phi2 = exp(-2 * c_fd2 * ix**2)
    g2 = phi2 * g_0 + (1 - phi2) * g_inf
    c2 = c_fd2 * g2 * sigma_inf / (2 * pi)
    # if sigma_bound > 1:
    #     kappa_bound = (1 + alpha_q) * sigma_bound / (1 - (2 - sigma_bound) ** (alpha_q + 1))
    # else:
    kappa_bound = (1 + alpha_q) * sigma_bound / (1 - (1 - sigma_bound) ** (alpha_q + 1))

    kappa_1 = 1 + alpha_q  # каппа при кси = 1

    delta_s = (
        log((sigma_bound + kappa_bound * c1) / (sigma_w + kappa_bound * c1))
        + log((1 + kappa_1 * c2) / (sigma_w + kappa_1 * c2))
        - log((sigma_bound + kappa_bound * c2) / (sigma_w + kappa_bound * c2))
    )

    return 1 / (log(beta_re * re / xf) + log(sigma_inf) + delta_s)


def calc_j_from_j_d(j_d: float, k: float, h: float, mu: float, fvf: float) -> float:
    """
    Функция обратного преобразования от безразмерного Кпрод к размерному Кпрод

    Parameters
    ----------
    :param j_d: Безразмерный Кпрод
    :param k: проницаемость пласта, м^2
    :param h: мощность пласта, м
    :param mu: Вязкость жидкости, Па*с.
    :param fvf: объёмный коэффициент

    :return: коэффициент продуктивности, м3*сут/МПа
    -------
    """
    if j_d is not None:
        j = (2 * pi * k * h / (mu * fvf)) * j_d
        j = j * 10**6 * 86400  # Перевод в м^3/(сут*МПа)
    else:
        j = None
    return j


def calc_sigma_from_x(x: float, rw: float, sigma_w: float, xf: float) -> float:
    """
    Функция преобразования координат от x к sigma

    Parameters
    ----------
    :param x: координата по x
    :param rw: радиус скважины, м
    :param sigma_w:
    :param xf: длина трещины, м

    :return: безразмерная координата
    -------
    """
    if x == xf:
        return 1
    else:
        return sigma_w + (1 - sigma_w) * (x - rw) / (xf - rw)


def calc_sigma_inf(ix: float, lambd: float) -> float:
    """
    Функция расчёта обратного безразмерного радиуса скважины от коэффициента проникновения трещины ix и
    параметра соотношения сторон lambd

    Parameters
    ----------
    :param ix: коэффициент проникновения трещины, (д.ед.)
    :param lambd: коэффиицент, характеризующий соотношение сторон пласта xe/ye

     :return: обратный безразмерный радиус скважины
    -------

    График считан по точкам из статьи Meyer fig.D3
    """
    # Создаем массивы для ix, lambd, r
    i_x = np.zeros(11)

    dim_r_l1 = np.zeros(11)
    dim_r_l2 = np.zeros(11)
    dim_r_l4 = np.zeros(11)
    dim_r_l6 = np.zeros(11)
    dim_r_l8 = np.zeros(11)
    dim_r_l10 = np.zeros(11)

    lambd_x = np.zeros(6)
    r_lambd_y = np.zeros(6)

    lambd_x[0] = 1
    lambd_x[1] = 2
    lambd_x[2] = 4
    lambd_x[3] = 6
    lambd_x[4] = 8
    lambd_x[5] = 10

    i_x[0] = 0
    i_x[1] = 0.1
    i_x[2] = 0.2
    i_x[3] = 0.3
    i_x[4] = 0.4
    i_x[5] = 0.5
    i_x[6] = 0.6
    i_x[7] = 0.7
    i_x[8] = 0.8
    i_x[9] = 0.9
    i_x[10] = 1

    dim_r_l1[0] = 2
    dim_r_l1[1] = 2.01
    dim_r_l1[2] = 2.025
    dim_r_l1[3] = 2.06
    dim_r_l1[4] = 2.125
    dim_r_l1[5] = 2.2
    dim_r_l1[6] = 2.316
    dim_r_l1[7] = 2.46
    dim_r_l1[8] = 2.65
    dim_r_l1[9] = 2.825
    dim_r_l1[10] = 3.125

    dim_r_l2[0] = 2
    dim_r_l2[1] = 2
    dim_r_l2[2] = 2
    dim_r_l2[3] = 2.016
    dim_r_l2[4] = 2.05
    dim_r_l2[5] = 2.1
    dim_r_l2[6] = 2.183
    dim_r_l2[7] = 2.3125
    dim_r_l2[8] = 2.475
    dim_r_l2[9] = 2.666
    dim_r_l2[10] = 2.866

    dim_r_l4[0] = 2
    dim_r_l4[1] = 1.95
    dim_r_l4[2] = 1.8166
    dim_r_l4[3] = 1.675
    dim_r_l4[4] = 1.55
    dim_r_l4[5] = 1.475
    dim_r_l4[6] = 1.45
    dim_r_l4[7] = 1.466
    dim_r_l4[8] = 1.533
    dim_r_l4[9] = 1.65
    dim_r_l4[10] = 1.766

    dim_r_l6[0] = 2
    dim_r_l6[1] = 1.85
    dim_r_l6[2] = 1.5
    dim_r_l6[3] = 1.216
    dim_r_l6[4] = 1
    dim_r_l6[5] = 0.875
    dim_r_l6[6] = 0.8
    dim_r_l6[7] = 0.766
    dim_r_l6[8] = 0.783
    dim_r_l6[9] = 0.825
    dim_r_l6[10] = 0.883

    dim_r_l8[0] = 2
    dim_r_l8[1] = 1.716
    dim_r_l8[2] = 1.216
    dim_r_l8[3] = 0.833
    dim_r_l8[4] = 0.616
    dim_r_l8[5] = 0.475
    dim_r_l8[6] = 0.4
    dim_r_l8[7] = 0.366
    dim_r_l8[8] = 0.366
    dim_r_l8[9] = 0.375
    dim_r_l8[10] = 0.4

    dim_r_l10[0] = 2
    dim_r_l10[1] = 1.566
    dim_r_l10[2] = 0.933
    dim_r_l10[3] = 0.55
    dim_r_l10[4] = 0.35
    dim_r_l10[5] = 0.233
    dim_r_l10[6] = 0.183
    dim_r_l10[7] = 0.166
    dim_r_l10[8] = 0.15
    dim_r_l10[9] = 0.151
    dim_r_l10[10] = 0.175

    # Определяем функции, описывающие зависимость б/р радиуса от коэффициента проникновения при различных lambd
    f_r_target_l1 = interp1d(i_x, dim_r_l1, kind='cubic', fill_value="extrapolate")
    f_r_target_l2 = interp1d(i_x, dim_r_l2, kind='cubic', fill_value="extrapolate")
    f_r_target_l4 = interp1d(i_x, dim_r_l4, kind='cubic', fill_value="extrapolate")
    f_r_target_l6 = interp1d(i_x, dim_r_l6, kind='cubic', fill_value="extrapolate")
    f_r_target_l8 = interp1d(i_x, dim_r_l8, kind='cubic', fill_value="extrapolate")
    f_r_target_l10 = interp1d(i_x, dim_r_l10, kind='cubic', fill_value="extrapolate")

    # Рассчитываем б/р радиус при заданном значении ix
    r_lambd_y[0] = f_r_target_l1(ix)
    r_lambd_y[1] = f_r_target_l2(ix)
    r_lambd_y[2] = f_r_target_l4(ix)
    r_lambd_y[3] = f_r_target_l6(ix)
    r_lambd_y[4] = f_r_target_l8(ix)
    r_lambd_y[5] = f_r_target_l10(ix)

    # Определяем функцию, описывающую зависимость б/р радиуса от lambd
    f_r_lambd = interp1d(lambd_x, r_lambd_y, kind='cubic', fill_value="extrapolate")

    return f_r_lambd(lambd)
