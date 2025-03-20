import pandas as pd
from app.card_handlers.simple_gdis_calculate.src.Fluid_info import FormationInfo
from app.card_handlers.base.exceptions import CardHandlerException
from app.card_handlers.simple_gdis_calculate.src.Hydrodynamic_Data import (
    HydrodynamicData,
)


def read_excel_data(file_content: pd.ExcelFile) -> HydrodynamicData:
    """
    Функция считывания гидродинамических исследований из файла Excel и помещения их в класс HydrodynamicData.

    :param file_content: Открытый Excel-файл.
    :return: Экземпляр класса HydrodynamicData.
    """
    try:
        # Читаем данные с основного листа
        df = file_content.parse(usecols="A:B", header=0).dropna()

        # Извлечение данных delta t и delta P
        delta_t_values = df.iloc[:, 0].tolist()
        delta_p_values = df.iloc[:, 1].tolist()

        # Считывание метода интерпретации
        interpretation_method = file_content.parse(
            usecols="I", nrows=3, header=None
        ).iloc[2, 0]
    except Exception as e:
        raise CardHandlerException(f"Ошибка при считывании данных из Excel: {e}")

    return HydrodynamicData(
        delta_t=delta_t_values, delta_p=delta_p_values, method=interpretation_method
    )


def read_formation_info(file_content: pd.ExcelFile) -> FormationInfo:
    """
    Функция считывания параметров пласта и флюида из файла Excel и записи их в класс FormationInfo.

    :param file_content: Открытый Excel-файл.
    :return: Экземпляр класса FormationInfo со считанными параметрами.
    """
    try:
        # Читаем нужные данные из Excel
        df = file_content.parse(usecols="E", nrows=7, header=None)

        # Извлекаем параметры пласта и флюида
        Q, b, density, h, mu, c_total, distance = df.iloc[:, 0].tolist()

        # Создаем объект FormationInfo с полученными параметрами
        return FormationInfo(
            Q=Q, b=b, density=density, h=h, mu=mu, c_total=c_total, distance=distance
        )

    except Exception as e:
        raise CardHandlerException(
            f"Ошибка при считывании параметров пласта и флюида: {e}"
        )


# Выводим результат
# print("Параметры пласта и флюида после пересчета:")
# print(FormationInfo)
