from pathlib import Path
import pandas as pd
from app.card_handlers.pseudosoil.src.data_class import (
    WellParameters,
    LabExperimentData,
)


def get_selected_case(file_content: pd.ExcelFile, sheet_name: str = "Капилляры и трещины") -> str:
    """
    Функция считывания выбранного случая из файла Excel.

    :param file_content: Открытый Excel file.
    :param sheet_name: Название листа Excel, из которого нужно считать случай (по умолчанию "Капилляры и трещины").
    :return: Строка с названием выбранного случая.
    """
    # Считываем выбранный случай из Excel
    selected_case = file_content.parse(
        usecols="B",  # Считываем только колонку B
        sheet_name=sheet_name,
        nrows=1,  # Считываем только первую строку
        header=None,  # Не используем заголовок
    ).iloc[
        0, 0
    ]  # Получаем значение из первой ячейки

    return selected_case


def read_parameters_isotropic(file_content: pd.ExcelFile):
    """
    Функция считывания параметров эффективной изотропной среды из файла Excel в зависимости от выбранного случая.

    :param file_content: Открытый Excel файл.
    :return: Кортеж, содержащий соответствующие параметры в зависимости от выбранного случая.
    """
    # global selected_case
    selected_case = get_selected_case(
        file_content
    )  # Считываем выбранный случай через отдельную функцию

    if selected_case is None:
        print("Ошибка: Не удалось считать выбранный случай.")
        return None

    try:
        # Считываем выбранный случай из Excel-файла
        selected_case = file_content.parse(
            usecols=("B"),
            sheet_name="Капилляры и трещины",
            nrows=1,
            header=None,
        ).iloc[0, 0]

        # Считываем параметры в зависимости от выбранного случая
        if selected_case == "Одинаковые капилляры":
            r0 = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=5,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            n = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=5,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            d = file_content.parse(
                usecols="E",
                sheet_name="Капилляры и трещины",
                skiprows=5,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return r0, n, d, selected_case

        if selected_case == "Капилляры с равномерным распределением":
            rmin = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=9,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            rmax = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=9,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            n = file_content.parse(
                usecols="E",
                sheet_name="Капилляры и трещины",
                skiprows=9,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            d = file_content.parse(
                usecols="F",
                sheet_name="Капилляры и трещины",
                skiprows=9,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x1 = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y1 = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x2 = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y2 = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x3 = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y3 = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return rmin, rmax, n, d, x1, y1, x2, y2, x3, y3, selected_case

        if selected_case == "Капилляры с неравномерным распределением":
            rmin = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=13,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            rmax = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=13,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            n = file_content.parse(
                usecols="E",
                sheet_name="Капилляры и трещины",
                skiprows=13,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            d = file_content.parse(
                usecols="F",
                sheet_name="Капилляры и трещины",
                skiprows=13,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x1 = file_content.parse(
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y1 = file_content.parse(
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x2 = file_content.parse(
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y2 = file_content.parse(
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x3 = file_content.parse(
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y3 = file_content.parse(
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return rmin, rmax, n, d, x1, y1, x2, y2, x3, y3, selected_case

        if selected_case == "Одинаковые трещины":
            w = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=17,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            xi = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=17,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return w, xi, selected_case

        if selected_case == "Трещины с равномерным распределением":
            wmin = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=21,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            wmax = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=21,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            xi = file_content.parse(
                usecols="E",
                sheet_name="Капилляры и трещины",
                skiprows=21,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x1 = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y1 = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x2 = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y2 = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x3 = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y3 = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return wmin, wmax, xi, x1, y1, x2, y2, x3, y3, selected_case

        if selected_case == "Трещины с неравномерным распределением":
            wmin = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=25,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            wmax = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=25,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            xi = file_content.parse(
                usecols="E",
                sheet_name="Капилляры и трещины",
                skiprows=25,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x1 = file_content.parse(
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y1 = file_content.parse(
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x2 = file_content.parse(
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y2 = file_content.parse(
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x3 = file_content.parse(
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y3 = file_content.parse(
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return wmin, wmax, xi, x1, y1, x2, y2, x3, y3, selected_case

        if selected_case == "Расчет радиуса поры":
            k = file_content.parse(
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=29,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            phi = file_content.parse(
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=29,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return k, phi, selected_case

    except Exception as e:
        print(f"Ошибка при считывании параметров: {e}")
        return None


def read_parameters_lab(file_content: pd.ExcelFile) -> LabExperimentData:
    """
    Функция считывания параметров лабораторного эксперимента с указанного листа Excel.

    :param file_content: Открытый Excel файл.
    :return: Объект класса LabExperimentData, содержащий считанные параметры.
    """
    # Считываем с Excel-файла необходимые значения с листа "Данные лаб. эксперимента"
    df = file_content.parse(sheet_name="Данные лаб. эксперимента", usecols="B:D").dropna()

    # Создаем пустой список, в котором храним считанные значения
    df["Значения"] = df["Значения"].astype(float)

    # Извлечение необходимых значений
    data = [float(i) for i in df["Значения"]]
    d, m, mu, l = data[0], data[1], data[2], data[3]

    # Считываем массив со значениями k и расхода с того же листа
    df2 = file_content.parse(
        usecols="E:F",
        skiprows=range(0, 9),
        nrows=10,
        header=None,
        sheet_name="Данные лаб. эксперимента",
    )
    df2.columns = ["k", "Расход, см3/c"]

    # Преобразование считанных данных в списки
    k_values = df2["k"].tolist()
    flow_values = df2["Расход, см3/c"].tolist()

    # Создание и возврат объекта класса LabExperimentData
    return LabExperimentData(d, m, mu, l, k_values, flow_values)


def read_parameters_well(file_content: pd.ExcelFile) -> WellParameters:
    """
    Функция считывания параметров работы скважины.

    :param file_content: Открытый Excel файл.
    :return: Объект класса WellParameters, содержащий считанные параметры.
    """
    # Считывание параметров скважины из столбца B на листе "Данные по скважине"
    length_filter = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=1,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    well_diameter = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=2,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    perforation_density = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=3,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    hole_diameter = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=4,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    oil_density = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=5,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    oil_volume_factor = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=6,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    reservoir_oil_viscosity = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=7,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    well_spacing = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=8,
        nrows=1,
        header=None,
    ).iloc[0, 0]

    # Считывание параметров режима скважины из столбца F на листе "Данные по скважине"
    bottomhole_pressure = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="F",
        skiprows=1,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    reservoir_pressure = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="F",
        skiprows=2,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    flow_rate = file_content.parse(
        sheet_name="Данные по скважине",
        usecols="F",
        skiprows=3,
        nrows=1,
        header=None,
    ).iloc[0, 0]

    # Создание объекта класса WellParameters со считанными параметрами
    return WellParameters(
        length_filter,
        well_diameter,
        perforation_density,
        hole_diameter,
        oil_density,
        oil_volume_factor,
        reservoir_oil_viscosity,
        well_spacing,
        bottomhole_pressure,
        reservoir_pressure,
        flow_rate,
    )
