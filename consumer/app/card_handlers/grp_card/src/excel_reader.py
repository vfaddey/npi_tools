import numpy as np
import pandas as pd
from .data import WellProperty, SeamProperty, AuxiliaryProperty
import pandas as pd

# Изменил функцию считывания данных из экселя, чтобы на вход подавался не путь, а pd.ExcelFile


def load_excel_data(file_content: pd.ExcelFile):
    """Загружает данные из Excel и возвращает параметры"""

    try:
        # Загружаем лист "Исходные данные"
        sheet_name = 'Исходные данные'
        if sheet_name not in file_content.sheet_names:
            raise ValueError(f"Лист '{sheet_name}' не найден в файле.")

        ws = file_content.parse(sheet_name, header=None)  # Читаем без заголовков

        # Проверка на пустой лист
        if ws.empty:
            raise ValueError(f"Лист '{sheet_name}' пуст.")

        # Создаем словарь для перевода столбцов (A → 0, B → 1, C → 2, ...)
        col_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}

        # Функция для извлечения значения из DataFrame по адресу Excel (например, "C2")
        def get_value(cell: str):
            col_letter, row_number = cell[0], int(cell[1:]) - 1
            col_index = col_map.get(col_letter)

            if col_index is None:
                raise ValueError(f"Ошибка: столбец {col_letter} не найден в col_map!")

            try:
                return ws.iloc[row_number, col_index]
            except IndexError:
                raise ValueError(f"Ошибка: ячейка {cell} выходит за границы данных.")

        # Извлечение данных для SeamProperty
        seams = SeamProperty(
            get_value('C2'),  # Проницаемость пласта, м^2
            get_value('C3'),  # Объемный коэффициент
            get_value('C4'),  # Вязкость жидкости, Па*с
            get_value('C5'),  # Толщина пласта, м
            get_value('C6'),  # Радиус зоны дренирования, м
            get_value('C7'),  # Размер зоны дренирования по оси X, м
            get_value('C8'),  # Размер зоны дренирования по оси Y, м
            get_value('C9')  # Начальное пластовое давление, Па
        )
        # Извлечение данных для WellProperty
        well = WellProperty(
            get_value('C12'),  # Дебит скважины, м³/с
            get_value('C13'),  # Радиус скважины, м
            get_value('C14'),  # Половина длины трещины, м
            get_value('C15'),  # Проницаемость трещины, м²
            get_value('C16'),  # Ширина трещины, м
            None  # Доп. параметр, если нужен
        )

        # Извлечение данных для AuxiliaryProperty
        aux = AuxiliaryProperty(
            get_value('C19'),  # Начальная координата
            get_value('C20'),  # Точность
            get_value('C21'),  # Шаг вычисления притока
            get_value('C22'),  # Проницаемость загрязненной зоны
            get_value('C23'),  # Точка начала загрязненной зоны
            np.flip(ws.iloc[1:21, col_map['E']].values).tolist()  # Длина загрязненной зоны
        )

        return seams, well, aux

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return None, None, None
