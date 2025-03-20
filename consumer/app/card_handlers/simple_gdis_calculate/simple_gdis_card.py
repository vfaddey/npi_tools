from pathlib import Path
import pandas as pd

from app.card_handlers.base.exceptions import CardHandlerException
from app.card_handlers.base.utils import print_work_time
from app.card_handlers.simple_gdis_calculate.src.excel_reader import (
    read_excel_data,
)
from app.card_handlers.simple_gdis_calculate.src.mdh_interpretation import (
    calculate_lg_t,
    calculate_mdh,
)
from app.card_handlers.simple_gdis_calculate.src.excel_reader import read_formation_info
from app.card_handlers.base.card_handler import (
    CardHandler,
    HandlerResult,
    ResultParameter,
)
from app.entities.card import CardType


class SimpleGDISHandler(CardHandler):
    CARD_TYPE = "SIMPLEGDIS"  # CardType.SIMPLEGDIS

    @print_work_time
    def process(self, data) -> HandlerResult:
        """
        Основной метод обработки данных.
        :param data: Входные данные, содержащие байты Excel-файла
        :return: HandlerResult с рассчитанными параметрами в JSON
        """

        try:
            file_content = pd.ExcelFile(data)

            if not data.name.endswith(".xlsx"):
                raise CardHandlerException("Ожидается файл с расширением .xlsx")

            hydrodynamic_data = read_excel_data(file_content)
            lg_t_result = calculate_lg_t(hydrodynamic_data)
            delta_p = hydrodynamic_data.delta_p
            coef_angle_incl = (delta_p[-1] - delta_p[-9]) / (
                lg_t_result[-1] - lg_t_result[-9]
            )
            inter_segment = delta_p[-9] - coef_angle_incl * lg_t_result[-9]

            formation_info = read_formation_info(file_content)
            formation_info.recalibrate_Q()

            epsilon, param, piezo, k_prod, k = calculate_mdh(
                formation_info=formation_info,
                coef_angle_incl=coef_angle_incl,
                inter_segment=inter_segment,
            )

            # Формирование результата в JSON
            result = HandlerResult(
                data=[
                    ResultParameter(
                        value=epsilon,
                        name="epsilon",
                        translation="Гидропроводность пласта",
                    ),
                    ResultParameter(
                        value=param, name="param", translation="Комплексный параметр"
                    ),
                    ResultParameter(
                        value=piezo, name="piezo", translation="Пьезопроводность пласта"
                    ),
                    ResultParameter(
                        value=k_prod,
                        name="K_prod",
                        translation="Коэффициент продуктивности",
                    ),
                    ResultParameter(value=k, name="k", translation="Проницаемость"),
                ],
                assets=[],
            )

            return result
        except Exception as e:
            raise CardHandlerException(f"Ошибка обработки данных: {e}")

    def validate(self, data):
        """
        Метод проверки входных данных.
        """
        if "input_file" not in data:
            raise ValueError("Отсутствует обязательный параметр: input_file")


if __name__ == "__main__":
    # Пример Подключение обработчика
    handler = SimpleGDISHandler()

    # Подготовка данных
    data = {
        "input_file": str(Path(__file__).parent / "Входной файл.xlsx"),
    }

    # Вызов обработчика
    try:
        result = handler.process(data)
        print("Результаты обработки:")
        print(result.data)  # JSON данные
    except Exception as e:
        print(f"Ошибка при выполнении обработчика: {e}")
