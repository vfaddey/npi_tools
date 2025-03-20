import matplotlib.pyplot as plt
import numpy as np
import copy
from io import BytesIO
from .productivity_coefficient import ProductivityCoefficient


def generate_flow_distribution_graph(prod_coef) -> dict:
    """
    Генерация графика распределения потока.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(prod_coef.aux_props.array_x_axes_smooth, prod_coef.well_props.array_accumulated_flow_in_fracture,
             color='r', label='Накопленный поток в трещине', linestyle='dashed')
    plt.plot(prod_coef.aux_props.array_x_axes_smooth, prod_coef.well_props.array_flow_along_fracture,
             label='Адаптация параметра alpha')
    plt.xlabel('x, м')
    plt.ylabel('Q, м3/сут')
    plt.title('Распределение притока в трещине')
    plt.legend()
    plt.grid()

    return _save_plot_to_bytes("flow_distribution_graph.png")


def generate_productivity_coef_graph(seams, well, aux) -> dict:
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

    return _save_plot_to_bytes("productivity_coef_graph.png")


def _save_plot_to_bytes(filename: str) -> dict:
    """
    Сохраняет текущий график в байтовый формат и возвращает его данные.

    :param filename: Имя файла.
    :return: Словарь с данными графика.
    """
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format="png", dpi=200)
    plt.close()
    img_bytes.seek(0)

    return {
        "filename": filename,
        "bytes": img_bytes.getvalue(),
        "mime_type": "image/png",
        "extension": "png",
    }
