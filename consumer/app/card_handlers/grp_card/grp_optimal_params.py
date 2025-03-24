import pandas as pd

from app.card_handlers.grp_card.src.excel_reader import load_excel_data
from app.card_handlers.grp_card.src.productivity_coefficient import ProductivityCoefficient
from app.card_handlers.grp_card.src.plot_generator import generate_flow_distribution_graph, generate_productivity_coef_graph

from app.card_handlers.base.exceptions import CardHandlerException
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
            file_content = pd.ExcelFile(data)
            if not data.name.endswith('.xlsx'):
                raise CardHandlerException("Ожидается файл с расширением .xlsx")

            # Загрузка данных
            seams, well, aux = load_excel_data(file_content)
            if seams is None or well is None or aux is None:
                raise ValueError("Ошибка: данные не загружены, расчет не выполнен.")

            # Расчет коэффициента продуктивности
            prod_coef = ProductivityCoefficient(seam_props=seams, well_props=well, aux_props=aux)
            prod_coef.calc_prod_coef()

            # Подготовка данных для графиков
            graph_1 = generate_flow_distribution_graph(prod_coef)
            graph_2 = generate_productivity_coef_graph(seams, well, aux)

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
                    DataAsset(name="График распределения притока", file_format=".png", asset_type="graph", data=graph_1['bytes']),
                    DataAsset(name="График зависимости продуктивности", file_format=".png", asset_type="graph", data=graph_2['bytes']),
                ]
            )
            print(type(graph_1))
            return result
        except Exception as e:
            raise CardHandlerException(f"Ошибка при обработке данных: {e}")

    def validate(self, data):
        """
        Метод проверки входных данных.
        """
        required_keys = ["input_file"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Отсутствует обязательный параметр: {key}")


if __name__ == '__main__':
    handler = GrpCardHandler()

    try:
        # тут по идее подаются байты
        filename = 'Входной файл.xlsx'
        with open(filename, 'rb') as file:
            result = handler.process(file)
            print("Результаты обработки:")
            print(result.data)  # JSON данные
            print("Графики и файлы:")
            for asset in result.assets:
                print(f"{asset.asset_type}: {asset.data}")
    except Exception as e:
        print(f"Ошибка при выполнении обработчика: {e}")