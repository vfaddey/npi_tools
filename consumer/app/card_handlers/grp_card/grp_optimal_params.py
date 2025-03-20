import json
import copy
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from app.card_handlers.grp_card.src.excel_reader import load_excel_data
from app.card_handlers.grp_card.src.productivity_coefficient import ProductivityCoefficient
from app.card_handlers.base.utils import print_work_time
from app.card_handlers.base.card_handler import (
    CardHandler,
    HandlerResult,
    DataAsset,
    ResultParameter,
)
from app.entities.card import CardType


class GrpCardHandler(CardHandler):
    CARD_TYPE = CardType.GRP

    @print_work_time
    def process(self, data) -> HandlerResult:
        """
        Основной метод обработки данных.
        """
        try:
            # Загрузка данных
            seams, well, aux = load_excel_data(data["input_file"])
            if seams is None or well is None or aux is None:
                raise ValueError("Ошибка: данные не загружены, расчет не выполнен.")

            # Расчет коэффициента продуктивности
            prod_coef = ProductivityCoefficient(seam_props=seams, well_props=well, aux_props=aux)
            prod_coef.calc_prod_coef()

            # Подготовка данных для графиков
            graph_1 = self.generate_flow_distribution_graph(prod_coef)
            graph_2 = self.generate_productivity_coef_graph(seams, well, aux)

            # Формирование параметров результата
            result_data = [
                ResultParameter(name="flow_distribution", translation="Распределение притока",
                                value=prod_coef.well_props.array_flow_along_fracture),
                ResultParameter(name="productivity_coef", translation="Коэффициент продуктивности",
                                value=prod_coef.well_props.array_prod_coef_tail),
            ]

            # Формирование итогового результата
            result = HandlerResult(
                data=result_data,
                assets=[
                    DataAsset("График распределения притока", "graph_1", ".png", graph_1),
                    DataAsset("График зависимости продуктивности", "graph_2", ".png", graph_2),
                ]
            )
            return result
        except Exception as e:
            raise CardHandlerException(f"Ошибка при обработке данных: {e}")

    @staticmethod
    def generate_flow_distribution_graph(prod_coef):
        """
        Генерация графика распределения потока.
        """
        plt.figure(figsize=(10, 5))
        plt.plot(prod_coef.aux_props.array_x_axes_smooth, prod_coef.well_props.array_accumulated_flow_in_fracture,
                 color='r',
                 label='Накопленный поток в трещине', linestyle='dashed')
        plt.plot(prod_coef.aux_props.array_x_axes_smooth, prod_coef.well_props.array_flow_along_fracture,
                 label='Адаптация параметра alpha')
        plt.xlabel('x, м')
        plt.ylabel('Q, м3/сут')
        plt.title('Распределение притока в трещине')
        plt.legend()
        plt.grid()
        graph_path = 'flow_distribution_graph.png'
        plt.savefig(graph_path)
        plt.close()
        return graph_path

    @staticmethod
    def generate_productivity_coef_graph(seams, well, aux):
        """
        Генерация графика зависимости продуктивности от загрязненности.
        """
        k_f_tail_values = [7E-11, 3E-11, 9E-12, aux.k_f_tail]
        plt.figure(figsize=(10, 5))
        aux_copy = copy.deepcopy(aux)

        for k_f_tail in k_f_tail_values:
            aux_copy.k_f_tail = k_f_tail
            prod_coef = ProductivityCoefficient(seam_props=seams, well_props=well, aux_props=aux_copy)
            prod_coef.calc_prod_coef()
            plt.plot(
                np.flip(prod_coef.aux_props.array_lenght_dirt),
                prod_coef.well_props.array_prod_coef_tail,
                label=f'k_f_tail = {k_f_tail:.2e}'
            )

        plt.xlabel('Длина загрязнения, м')
        plt.ylabel('Безразмерный коэффициент продуктивности')
        plt.title('Зависимость продуктивности трещины от её загрязненности')
        plt.grid()
        plt.legend()
        graph_path = 'productivity_coef_graph.png'
        plt.savefig(graph_path)
        plt.close()
        return graph_path

    def validate(self, data):
        """
        Метод проверки входных данных.
        """
        required_keys = ["input_file"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Отсутствует обязательный параметр: {key}")


if __name__ == '__main__':
    # Пример Подключение обработчика
    handler = GrpCardHandler()

    # Подготовка данных
    data = {
        "input_file": str(Path(__file__).parent / "Входной файл.xlsx"),  # путь к файлу
    }

    # Вызов обработчика
    try:
        result = handler.process(data)
        print("Результаты обработки:")
        result_data = {}

        for param in result.data:
            value = param.value
            # Проверяем, является ли объект массивом NumPy, и преобразуем в список
            if isinstance(value, np.ndarray):
                value = value.tolist()

            print(f"{param.translation}: {value}")  # Печать результатов
            result_data[param.name] = value  # Добавление в JSON

        # Сохранение результатов в JSON
        json_result = json.dumps(result_data, indent=4, ensure_ascii=False)
        json_path = Path(__file__).parent / "output_data.json"
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json_result)

        print(f"Данные сохранены в {json_path}")

        print("Графики:")
        for asset in result.assets:
            print(f"{asset.asset_type}: {asset.data}")  # Печать путей к графикам

    except Exception as e:
        print(f"Ошибка при выполнении обработчика: {e}")

