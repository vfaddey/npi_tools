import numpy as np
from .data import WellProperty, SeamProperty, AuxiliaryProperty

# Изменил функцию считывания данных из экселя, чтобы на вход подавался не путь, а pd.ExcelFile


def load_excel_data(file_content: pd.ExcelFile):
    """Загружает данные из Excel и возвращает параметры"""

    try:
        # Ожидаем, что file_content - это экземпляр pd.ExcelFile
        # Проверка наличия листа "Исходные данные"
        if 'Исходные данные' not in file_content.sheet_names:
            raise ValueError("Лист 'Исходные данные' не найден в файле.")

        ws = file_content.parse('Исходные данные')

        # Проверяем, что важные данные не пустые
        required_cells = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                          'C12', 'C13', 'C14', 'C15', 'C16', 'C19', 'C20', 'C21', 'C22', 'C23']

        # Проверка значений ячеек, извлекая из DataFrame
        for cell in required_cells:
            if pd.isna(ws[cell].iloc[0]):
                raise ValueError(f"Отсутствует значение в ячейке {cell}")

        # Извлечение данных для SeamProperty
        seams = SeamProperty(
            ws['C2'].iloc[0],  # Проницаемость пласта, м^2
            ws['C3'].iloc[0],  # Объемный коэффициент
            ws['C4'].iloc[0],  # Вязкость жидкости, Па*с
            ws['C5'].iloc[0],  # Толщина пласта, м
            ws['C6'].iloc[0],  # Радиус зоны дренирования, м
            ws['C7'].iloc[0],  # Размер зоны дренирования по оси X, м
            ws['C8'].iloc[0],  # Размер зоны дренирования по оси Y, м
            ws['C9'].iloc[0]  # Начальное пластовое давление, Па
        )

        # Извлечение данных для WellProperty
        well = WellProperty(
            ws['C12'].iloc[0],  # Дебит скважины, м³/с
            ws['C13'].iloc[0],  # Радиус скважины, м
            ws['C14'].iloc[0],  # Половина длины трещины, м
            ws['C15'].iloc[0],  # Проницаемость трещины, м²
            ws['C16'].iloc[0],  # Ширина трещины, м
            None  # Доп. параметр, если нужен
        )

        # Извлечение данных для AuxiliaryProperty
        aux = AuxiliaryProperty(
            ws['C19'].iloc[0],  # Начальная координата
            ws['C20'].iloc[0],  # Точность
            ws['C21'].iloc[0],  # Шаг вычисления притока
            ws['C22'].iloc[0],  # Проницаемость загрязненной зоны
            ws['C23'].iloc[0],  # Точка начала загрязненной зоны
            np.flip(ws['E'][1:21].values).tolist()  # Длина загрязненной зоны
        )

        return seams, well, aux

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return None, None, None
