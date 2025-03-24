from .data import SeamProperty, WellProperty, AuxiliaryProperty
from .elliptical_fracture_chen_utils import *
from .tail_in_utils import *


class ProductivityCoefficient:
    seam_props: SeamProperty
    well_props: WellProperty
    aux_props: AuxiliaryProperty

    def __init__(self, seam_props: SeamProperty, well_props: WellProperty, aux_props: AuxiliaryProperty):
        self.seam_props = seam_props
        self.well_props = well_props
        self.aux_props = aux_props

    def calc_prod_coef(self):
        """
        DESCRIPTION:
        Функця calc_prod_coef позволяет определять
        коэффициенты продуктивности скважины с трещиной ГРП по различным методикам:

            - Расчет Кпрод по модели Chen (трещина эллиптической формы)
            - Расчет Кпрод по модели Meyer для модели Tail-in (проводимость трещины меняется на конце)

        OUTPUT:
        Массив значений притока вдоль трещины.
        Массив сглаженных значений притока.
        Массив значений безразмерного коэффициента продуктивности по модели Meyer для модели Tail-in.

        """

        # Переход к эллиптическим координатам
        ksi_e, ksi_1 = recalc_res_parameters(
            self.well_props.xf, self.well_props.width_fracture, self.seam_props.xe, self.seam_props.ye
        )

        # Определяем константы
        f_e, c, a_1, b_0, c_3, a_1_ = calc_constants(
            self.well_props.permeability_fracture,
            self.well_props.width_fracture,
            self.seam_props.permeability,
            self.well_props.xf,
            self.seam_props.viscosity,
            self.well_props.rate_well,
            self.seam_props.thickness,
            self.seam_props.reservoir_pressure,
            ksi_e,
            ksi_1,
        )

        # Определяем забойное давление
        # p_w = calc_pwf(ksi_e, ksi_1, self.seam_props.reservoir_pressure, f_e, c, c_3, self.aux_props.epsilon)
        # print('Рзаб = ', p_w, 'атм')

        # Определяем Кпрод
        j_d_chen = calc_jd_chen(
            self.seam_props.permeability,
            self.seam_props.thickness,
            self.seam_props.viscosity,
            ksi_e,
            f_e,
            a_1_,
            self.aux_props.epsilon,
        )
        # print('JD Chen', j_d_chen)

        # Расчет безразмерного коэффицента продуктивности
        j_d_dimensionless = calc_jd_pss_new(f_e, self.seam_props.radius_drainage, self.well_props.xf)
        # print('JD dimensionless', j_d_dimensionless)

        # Распределение притока вдоль трещины
        sum_qi, qi, qi_accum, x_axes = calc_qi(
            self.well_props.xf,
            self.aux_props.x_coordinate,
            self.seam_props.permeability,
            self.seam_props.thickness,
            self.seam_props.viscosity,
            self.seam_props.reservoir_pressure,
            ksi_e,
            ksi_1,
            f_e,
            c,
            self.aux_props.accuracy,
            self.aux_props.epsilon,
        )
        # print('Суммарный дебит скважины: ' + str(sum_qi))

        # Распределение давления вдоль трещины
        # p_fi = calc_p_fracture(
        #     self.well_props.xf,
        #     self.aux_props.x_coordinate,
        #     self.seam_props.reservoir_pressure,
        #     ksi_e,
        #     ksi_1,
        #     f_e,
        #     c,
        #     c_3,
        #     self.aux_props.accuracy,
        #     self.aux_props.epsilon,
        # )
        # print('Распределение давления вдоль трещины', p_fi)

        # Сглаживание графика распределения притока вдоль трещины
        x_axes_smooth, qi_smooth, qi_smooth_accum = smoothing_qi(qi, x_axes)
        # print('Массив координат:', x_axes_smooth)

        # Подбор alpha_q
        adapt_alpha_q = adaptation_alpha_q(qi_smooth_accum, x_axes_smooth, self.well_props.xf)
        # print('Адаптированный коэффициент alpha_q: ' + str(adapt_alpha_q))

        # Расчет массива с потоком вдоль трещины с заданным коэффициентом alpha_q
        q_calc = np.zeros(len(x_axes_smooth))
        q0 = qi_smooth_accum[0]
        std = 0

        for i in range(0, len(x_axes_smooth)):
            x_d = x_axes_smooth[i] / self.well_props.xf
            q_calc[i] = q0 * ((1 - x_d) ** adapt_alpha_q)
        # print(q_calc)

        ix = self.well_props.xf / self.seam_props.xe  # - коэффициент проникновения, ед.
        lambd = self.seam_props.xe / self.seam_props.ye  # - соотношение сторон пласта, xe/ye

        c_a = 30.88  # - Форм-фактор для скважины в центре квадратного пласта
        alpha_q = adapt_alpha_q  # - Fracture flux power coefficient
        sigma_inf = calc_sigma_inf(ix, lambd)
        sigma_w = self.well_props.radius_well * sigma_inf / self.well_props.xf

        # Инициализация массива для хранения результатов
        j_d_tail_in = np.zeros(len(self.aux_props.array_lenght_dirt))

        # Расчёт Кпрод по модели Meyer для модели Tail-in. (проводимость трещины меняется на конце)
        if self.aux_props.k_f_tail is not None or self.aux_props.tail_coordinate is not None:
            for i, dirt_coordinate in enumerate(self.aux_props.array_lenght_dirt):

                sigma_tail = calc_sigma_from_x(
                    dirt_coordinate, self.well_props.radius_well, sigma_w, self.well_props.xf*2
                )

                j_d_tail_in[i] = calc_j_d_finite_tail_in(
                    lambd,
                    sigma_inf,
                    sigma_w,
                    self.seam_props.radius_drainage,
                    alpha_q,
                    self.well_props.width_fracture,
                    self.seam_props.permeability,
                    c_a,
                    self.well_props.permeability_fracture,
                    self.aux_props.k_f_tail,
                    sigma_tail,
                    ix,
                    self.well_props.xf,
            )
            # print("Jd модель Tail-in: ", j_d_tail_in)

            j_tail_in = calc_j_from_j_d(
                j_d_tail_in,
                self.seam_props.permeability,
                self.seam_props.thickness,
                self.seam_props.viscosity,
                self.seam_props.volume_factor,
            )
            # print("Кпрод модель Tail-in: " + str(j_tail_in))
        else:
            j_d_tail_in = None

        self.well_props.array_flow_along_fracture = q_calc
        self.aux_props.array_x_axes_smooth = x_axes_smooth
        self.well_props.array_accumulated_flow_in_fracture = qi_smooth_accum
        self.well_props.array_prod_coef_tail = j_d_tail_in
