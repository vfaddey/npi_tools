# Определяем класс для хранения параметров скважины
class WellParameters:
    def __init__(
        self,
        length_filter: float,
        well_diameter: float,
        perforation_density: float,
        hole_radius: float,
        oil_density: float,
        oil_volume_factor: float,
        reservoir_oil_viscosity: float,
        well_spacing: float,
        bottomhole_pressure: float,
        reservoir_pressure: float,
        flow_rate: float,
    ):
        self.length_filter = length_filter  # Длина фильтра
        self.well_diameter = well_diameter  # Диаметр скважины
        self.perforation_density = perforation_density  # Плотность перфорации
        self.hole_radius = hole_radius  # Радиус отверстий перфорации
        self.oil_density = oil_density  # Плотность нефти
        self.oil_volume_factor = oil_volume_factor  # Объемный коэффициент нефти
        self.reservoir_oil_viscosity = (
            reservoir_oil_viscosity  # Вязкость нефти пластовой
        )
        self.well_spacing = well_spacing  # Расстояние между скважинами
        self.bottomhole_pressure = bottomhole_pressure  # Забойное давление
        self.reservoir_pressure = reservoir_pressure  # Пластовое давление
        self.flow_rate = flow_rate  # Приток


# Определение класса для хранения данных лабораторного эксперимента
class LabExperimentData:
    def __init__(
        self, d: float, m: float, mu: float, l: float, k_values: list, flow_values: list
    ):
        self.d = d  # Диаметр образца
        self.m = m  # Пористость образца
        self.mu = mu  # Вязкость жидкости
        self.l = l  # Длина образца
        self.k_values = k_values  # Список значений проницаемости
        self.flow_values = flow_values  # Список значений расхода
