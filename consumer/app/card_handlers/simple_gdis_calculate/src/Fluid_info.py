from dataclasses import dataclass


@dataclass
class FormationInfo:
    """
    Класс, содержащий информацию о пласте и флюиде.

    :param Q: Дебит жидкости, м^3/сут.
    :param b: Объемный коэфф. нефти, м^3/м^3.
    :param density: Плотность нефти, г/см^3
    :param h: Мощность пласта, м.
    :param mu: Вязкость нефти, сП.
    :param c_total: Общая сжимаемость, 1/атм.
    :param distance: Расстояние между скважинами, м.

    """

    Q: float
    b: float
    density: float
    h: float
    mu: float
    c_total: float
    distance: float

    def recalibrate_Q(self):
        """
        Функция пересчета м^3/сут в т/сут.
        """
        self.Q *= self.density
