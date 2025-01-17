from io import BytesIO
from pathlib import Path
from app.card_handlers.pseudosoil.src.pseudosoil_calculator import (
    calculate_case_1,
    calculate_case_2,
    calculate_case_3,
    calculate_case_4,
    calculate_case_5,
    calculate_case_6,
    calculate_case_7,
)
import matplotlib.pyplot as plt
import pandas as pd


def calculate_selected_case(parameters, file_content: pd.ExcelFile):
    """
    Функция, которая выполняет расчет в зависимости от выбранного случая.

    :param parameters: Кортеж считанных значеfile_content.parse()ний.
    :param file_path: Путь для считывания выбра

    :return: Результаты расчета в зависимости от выбранного случая.
    """
    # Считываем выбранный случай из Excel
    selected_case = file_content.parse(
        usecols="B",  # Считываем только колонку B
        sheet_name="Капилляры и трещины",
        nrows=1,  # Считываем только первую строку
        header=None,  # Не используем заголовок
    ).iloc[
        0, 0
    ]  # Получаем значение из первой ячейки
    print(f"Выбранный случай: {selected_case}")
    if selected_case == "Одинаковые капилляры":
        return calculate_case_1(parameters)
    elif selected_case == "Капилляры с равномерным распределением":
        return calculate_case_2(parameters)
    elif selected_case == "Капилляры с неравномерным распределением":
        return calculate_case_3(parameters)
    elif selected_case == "Одинаковые трещины":
        return calculate_case_4(parameters)
    elif selected_case == "Трещины с равномерным распределением":
        return calculate_case_5(parameters)
    elif selected_case == "Трещины с неравномерным распределением":
        return calculate_case_6(parameters)
    elif selected_case == "Расчет радиуса поры":
        return calculate_case_7(parameters)
    else:
        raise ValueError("Неизвестный случай")


def generate_plot(k_values_calculated, average_k_value) -> BytesIO:
    """
    Генерирует график результатов определения проницаемости и сохраняет его в формате SVG.

    :param k_values_calculated: Список рассчитанных значений проницаемости.
    :param average_k_value: Среднее значение проницаемости.
    :param output_path: Путь для сохранения графика (с расширением .svg).

    :return: None
    """
    # Создание графика
    plt.figure(figsize=(10, 6))

    # Нанесение точек на график для K_values_calculated
    plt.scatter(
        range(1, len(k_values_calculated) + 1),
        k_values_calculated,
        label="Результаты определения, мД",
    )

    # Нанесение прямой линии со значением average_k_value
    plt.axhline(
        y=average_k_value,
        color="r",
        linestyle="-",
        label="Среднее значение проницаемости, мД",
    )

    # Настройка подписей осей и заголовка графика
    plt.xlabel("Номер эксперимента")
    plt.ylabel("Результаты определения, мД")
    plt.title("Результаты определения проницаемости")
    plt.grid()
    # Добавление легенды
    plt.legend()

    output = BytesIO()

    # Сохранение графика в поток в формате SVG
    plt.savefig(output, format="svg")
    plt.close()

    # Перемотка потока в начало
    output.seek(0)

    return output


def save_results_to_excel(average_k_value: float, output_path_excel: Path) -> None:
    """
    Функция для создания DataFrame и записи среднего значения проницаемости в Excel файл.

    :param average_k_value: Среднее значение проницаемости, мД.
    :param output_path_excel: Среднее значение проницаемости, мД.

    """
    # Создание DataFrame с данными
    data = {"k, мД": [average_k_value]}
    average_df = pd.DataFrame(data)

    # Сохранение DataFrame в Excel файл по указанному пути
    average_df.to_excel(output_path_excel, index=False)


def save_permeability_to_excel(permeability: float, output_path_excel2: Path) -> None:
    """
    Функция для создания DataFrame и записи значения проницаемости в Excel файл.

    :param permeability: Значение проницаемости, мД.
    :param output_path_excel2: Путь до Excel файла, в который будет сохранено значение.
    """
    # Создание DataFrame с данными проницаемости
    data = {"Проницаемость по работе скважины, мД": [permeability]}
    permeability_df = pd.DataFrame(data)

    # Сохранение DataFrame в Excel файл по указанному пути
    permeability_df.to_excel(output_path_excel2, index=False)
