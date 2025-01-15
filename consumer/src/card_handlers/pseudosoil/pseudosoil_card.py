from pathlib import Path
from consumer.src.card_handlers.pseudosoil.src.results import (
    calculate_selected_case,
    generate_plot,
)
from consumer.src.card_handlers.pseudosoil.src.calculate_permeability import (
    calculate_entry_pressures,
    calculate_permeability,
    filter_outliers,
    calculate_average_permeability,
    well_performance_permeability,
)
from consumer.src.card_handlers.pseudosoil.src.excel_reader import (
    read_parameters_lab,
    read_parameters_isotropic,
    read_parameters_well,
)
from consumer.src.card_handlers.base.card_handler import (
    CardHandler,
    HandlerResult,
    DataAsset,
)
from producer.src.domain.entities.task import CardType


class PseudosoilHandler(CardHandler):
    CARD_TYPE = CardType.PSEUDOSOIL

    def process(self, data) -> HandlerResult:
        """
        Основной метод обработки данных.
        """
        try:
            # Путь к входному файлу
            base_path = Path(__file__).parent  # Директория, где лежит текущий файл
            file_path = base_path / "Входной файл.xlsx"
            output_path_graph = base_path / "output_graph.svg"  # Имя выходного файла

            # Проверка существования входного файла
            if not file_path.exists():
                raise FileNotFoundError(f"Входной файл не найден: {file_path}")

            # Расчет по лабораторным данным
            lab_exp_data = read_parameters_lab(file_path)
            p_vhod_values = calculate_entry_pressures(
                lab_exp_data, p_exit=101325, p_vhod=514317
            )
            k_values_calculated = calculate_permeability(lab_exp_data, p_vhod_values)
            k_verified = filter_outliers(k_values_calculated, multiplier=2)
            average_k_value = calculate_average_permeability(k_verified)
            generate_plot(k_values_calculated, average_k_value, output_path_graph)

            # Расчет изотропной среды
            parameters = read_parameters_isotropic(file_path)
            isotropic_results = calculate_selected_case(parameters, file_path)

            # Проницаемость по скважине
            well_param = read_parameters_well(file_path)
            well_permeability = well_performance_permeability(well_param)

            # Формирование результата
            result = HandlerResult(
                data={
                    "average_permeability": average_k_value,
                    "well_permeability": well_permeability,
                    "isotropic_results": isotropic_results,
                },
                assets=[
                    DataAsset("graph", ".svg", output_path_graph),
                ],
            )

            return result
        except Exception as e:
            raise Exception(f"Ошибка обработки данных: {e}")

    def validate(self, data):
        """
        Метод проверки входных данных.
        """
        required_keys = [
            "input_file",
            "output_graph",
        ]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Отсутствует обязательный параметр: {key}")


# Пример Подключение обработчика
handler = PseudosoilHandler()

# Подготовка данных
data = {
    "input_file": str(Path(__file__).parent / "Входной файл.xlsx"),  # путь к файлу
    "output_graph": "output_graph.svg",  # имя выходного графика
}

# Вызов обработчика
try:
    result = handler.process(data)
    print("Результаты обработки:")
    print(result.data)  # JSON данные
    print("Графики и файлы:")
    for asset in result.assets:
        print(f"{asset.asset_type}: {asset.data}")
except Exception as e:
    print(f"Ошибка при выполнении обработчика: {e}")
