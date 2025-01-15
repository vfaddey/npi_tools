from pathlib import Path
import pandas as pd
from consumer.src.card_handlers.pseudosoil.src.data_class import (
    WellParameters,
    LabExperimentData,
)


def get_selected_case(file_path: Path, sheet_name: str = "Капилляры и трещины") -> str:
    """
    Функция считывания выбранного случая из файла Excel.

    :param file_path: Путь к файлу Excel.
    :param sheet_name: Название листа Excel, из которого нужно считать случай (по умолчанию "Капилляры и трещины").
    :return: Строка с названием выбранного случая.
    """
    # Считываем выбранный случай из Excel
    selected_case = pd.read_excel(
        file_path,
        usecols="B",  # Считываем только колонку B
        sheet_name=sheet_name,
        nrows=1,  # Считываем только первую строку
        header=None,  # Не используем заголовок
    ).iloc[
        0, 0
    ]  # Получаем значение из первой ячейки

    return selected_case


def read_parameters_isotropic(file_path: Path):
    """
    Функция считывания параметров эффективной изотропной среды из файла Excel в зависимости от выбранного случая.

    :param file_path: Путь к файлу Excel с входными параметрами.
    :return: Кортеж, содержащий соответствующие параметры в зависимости от выбранного случая.
    """
    # global selected_case
    selected_case = get_selected_case(
        file_path
    )  # Считываем выбранный случай через отдельную функцию

    if selected_case is None:
        print("Ошибка: Не удалось считать выбранный случай.")
        return None

    try:
        # Считываем выбранный случай из Excel-файла
        selected_case = pd.read_excel(
            file_path,
            usecols=("B"),
            sheet_name="Капилляры и трещины",
            nrows=1,
            header=None,
        ).iloc[0, 0]

        # Считываем параметры в зависимости от выбранного случая
        if selected_case == "Одинаковые капилляры":
            r0 = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=5,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            n = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=5,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            d = pd.read_excel(
                file_path,
                usecols="E",
                sheet_name="Капилляры и трещины",
                skiprows=5,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return r0, n, d, selected_case

        if selected_case == "Капилляры с равномерным распределением":
            rmin = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=9,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            rmax = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=9,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            n = pd.read_excel(
                file_path,
                usecols="E",
                sheet_name="Капилляры и трещины",
                skiprows=9,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            d = pd.read_excel(
                file_path,
                usecols="F",
                sheet_name="Капилляры и трещины",
                skiprows=9,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x1 = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y1 = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x2 = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y2 = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x3 = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y3 = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return rmin, rmax, n, d, x1, y1, x2, y2, x3, y3, selected_case

        if selected_case == "Капилляры с неравномерным распределением":
            rmin = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=13,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            rmax = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=13,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            n = pd.read_excel(
                file_path,
                usecols="E",
                sheet_name="Капилляры и трещины",
                skiprows=13,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            d = pd.read_excel(
                file_path,
                usecols="F",
                sheet_name="Капилляры и трещины",
                skiprows=13,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x1 = pd.read_excel(
                file_path,
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y1 = pd.read_excel(
                file_path,
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x2 = pd.read_excel(
                file_path,
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y2 = pd.read_excel(
                file_path,
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x3 = pd.read_excel(
                file_path,
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y3 = pd.read_excel(
                file_path,
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return rmin, rmax, n, d, x1, y1, x2, y2, x3, y3, selected_case

        if selected_case == "Одинаковые трещины":
            w = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=17,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            xi = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=17,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return w, xi, selected_case

        if selected_case == "Трещины с равномерным распределением":
            wmin = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=21,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            wmax = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=21,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            xi = pd.read_excel(
                file_path,
                usecols="E",
                sheet_name="Капилляры и трещины",
                skiprows=21,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x1 = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y1 = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x2 = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y2 = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x3 = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y3 = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return wmin, wmax, xi, x1, y1, x2, y2, x3, y3, selected_case

        if selected_case == "Трещины с неравномерным распределением":
            wmin = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=25,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            wmax = pd.read_excel(
                file_path,
                usecols="D",
                sheet_name="Капилляры и трещины",
                skiprows=25,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            xi = pd.read_excel(
                file_path,
                usecols="E",
                sheet_name="Капилляры и трещины",
                skiprows=25,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x1 = pd.read_excel(
                file_path,
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y1 = pd.read_excel(
                file_path,
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=34,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x2 = pd.read_excel(
                file_path,
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y2 = pd.read_excel(
                file_path,
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=35,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            x3 = pd.read_excel(
                file_path,
                usecols="I",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            y3 = pd.read_excel(
                file_path,
                usecols="J",
                sheet_name="Капилляры и трещины",
                skiprows=36,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            return wmin, wmax, xi, x1, y1, x2, y2, x3, y3, selected_case

        if selected_case == "Расчет радиуса поры":
            k = pd.read_excel(
                file_path,
                usecols="C",
                sheet_name="Капилляры и трещины",
                skiprows=29,
                nrows=1,
                header=None,
            ).iloc[0, 0]
            phi = pd.read_excel(
                file_path,
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


def read_parameters_lab(file_path: Path) -> LabExperimentData:
    """
    Функция считывания параметров лабораторного эксперимента с указанного листа Excel.

    :param file_path: Путь к файлу Excel с входными параметрами.
    :return: Объект класса LabExperimentData, содержащий считанные параметры.
    """
    # Считываем с Excel-файла необходимые значения с листа "Данные лаб. эксперимента"
    df = pd.read_excel(file_path, usecols="B:D", sheet_name="Данные лаб. эксперимента")
    df = df.dropna()

    # Создаем пустой список, в котором храним считанные значения
    df["Значения"] = df["Значения"].astype(float)

    # Извлечение необходимых значений
    data = [float(i) for i in df["Значения"]]
    d, m, mu, l = data[0], data[1], data[2], data[3]

    # Считываем массив со значениями k и расхода с того же листа
    df2 = pd.read_excel(
        file_path,
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


def read_parameters_well(file_path: Path) -> WellParameters:
    """
    Функция считывания параметров работы скважины.

    :param file_path: Путь к файлу Excel с входными параметрами.
    :return: Объект класса WellParameters, содержащий считанные параметры.
    """
    # Считывание параметров скважины из столбца B на листе "Данные по скважине"
    length_filter = pd.read_excel(
        file_path,
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=1,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    well_diameter = pd.read_excel(
        file_path,
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=2,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    perforation_density = pd.read_excel(
        file_path,
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=3,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    hole_diameter = pd.read_excel(
        file_path,
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=4,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    oil_density = pd.read_excel(
        file_path,
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=5,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    oil_volume_factor = pd.read_excel(
        file_path,
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=6,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    reservoir_oil_viscosity = pd.read_excel(
        file_path,
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=7,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    well_spacing = pd.read_excel(
        file_path,
        sheet_name="Данные по скважине",
        usecols="B",
        skiprows=8,
        nrows=1,
        header=None,
    ).iloc[0, 0]

    # Считывание параметров режима скважины из столбца F на листе "Данные по скважине"
    bottomhole_pressure = pd.read_excel(
        file_path,
        sheet_name="Данные по скважине",
        usecols="F",
        skiprows=1,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    reservoir_pressure = pd.read_excel(
        file_path,
        sheet_name="Данные по скважине",
        usecols="F",
        skiprows=2,
        nrows=1,
        header=None,
    ).iloc[0, 0]
    flow_rate = pd.read_excel(
        file_path,
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
