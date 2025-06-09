import logging
from typing import Optional, Tuple, List
import os
import math

from PIL import Image, ImageDraw, ImageFont

from schemas import storage_schem, logic_schem

logger = logging.getLogger(__name__)


class Branch:
    """Объект помещения филиала, по которому будут рассчитываться
    координаты точек и оптимальные маршруты покупок
    """

    def __init__(self, exit_x: int, exit_y: int):
        # координаты входа на изображении
        self.exit_x = exit_x
        self.exit_y = exit_y

    def get_centroid(self, spots_list: List[storage_schem.spots_schem.SpotsWithShelvesSchem]) -> Tuple[int, int]:
        """Находим центроид между всеми точками.
        Данное действие необходимо чтобы отсечь удаленные точки
        в случае если один и тот же товар расположен на
        разных полках.
        Args:
            spots_list: список ячеек с координатами которые нужно посетить
        """
        logger.info(f"Вычисляю центроид для точек: {spots_list}")
        sum_x = sum([spot.x_spot_coord for spot in spots_list] + [self.exit_x])
        sum_y = sum([spot.y_spot_coord for spot in spots_list] + [self.exit_y])
        avg_x = sum_x // (len(spots_list) + 1)
        avg_y = sum_y // (len(spots_list) + 1)
        return avg_x, avg_y

    @staticmethod
    def distance_between_points(x1: int, y1: int, x2: int, y2: int) -> float:
        """Вычисляем расстояние между двумя точками"""
        logger.info(f"Замеряю дистанцию между точками: {x1}, {y1}, {x2}, {y2}")
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def nearest_neighbor(
            self,
            points: List[storage_schem.spots_schem.SpotsWithShelvesSchem]
    ) -> List[storage_schem.spots_schem.SpotsWithShelvesSchem]:
        """Строим маршрут для прохождения точек по ближайшим точкам
        Args:
            points: точки которые нужно посетить
        """
        unvisited = points.copy()
        path = list()
        current_x, current_y = self.exit_x, self.exit_y

        while unvisited:
            nearest = min(unvisited, key=lambda p: self.distance_between_points(current_x, current_y, p.x_spot_coord, p.y_spot_coord))
            path.append(nearest)
            current_x, current_y = nearest.x_spot_coord, nearest.y_spot_coord
            unvisited.remove(nearest)
        return path

    def two_opt(
            self,
            path: List[storage_schem.spots_schem.SpotsWithShelvesSchem]
    ) -> List[storage_schem.spots_schem.SpotsWithShelvesSchem]:
        improved = True
        while improved:
            improved = False
            for i in range(1, len(path) - 2):
                for j in range(i + 1, len(path) - 1):
                    # Получаем координаты точек
                    a_x, a_y = path[i - 1].x_spot_coord, path[i - 1].y_spot_coord
                    b_x, b_y = path[i].x_spot_coord, path[i].y_spot_coord
                    c_x, c_y = path[j].x_spot_coord, path[j].y_spot_coord
                    d_x, d_y = path[j + 1].x_spot_coord, path[j + 1].y_spot_coord

                    # Проверяем, что все координаты заданы
                    if None in [a_x, a_y, b_x, b_y, c_x, c_y, d_x, d_y]:
                        continue  # Пропускаем точки без координат

                    # Вычисляем расстояния
                    current_dist = (self.distance_between_points(a_x, a_y, b_x, b_y) +
                                    self.distance_between_points(c_x, c_y, d_x, d_y))
                    new_dist = (self.distance_between_points(a_x, a_y, c_x, c_y) +
                                self.distance_between_points(b_x, b_y, d_x, d_y))

                    if new_dist < current_dist:
                        # Разворачиваем отрезок между i и j
                        path[i:j + 1] = path[j:i - 1:-1]
                        improved = True
        return path

class Shelf:
    """Объект полки, который расположен в помещеннии и на котором располагаются
    товары"""
    def __init__(self, x1: int, y1: int, x2: int, y2: int, cell_count: int, floor_count: int = 1):
        # координаты начала полки на схеме помещения
        self.x1 = x1
        self.y1 = y1

        # координаты конца полки на схеме помещения
        self.x2 = x2
        self.y2 = y2

        # кол-во ячеек на полке по всей ее длине
        self.cell_count = cell_count

        # кол-во этажей на полке
        self.floor_count = floor_count

    def find_coord(self, cell_index: int) -> Tuple[int, int]:
        """Высчитываем координаты ячейки на полке.
        На вход поступает индекс ячейки на которой располагается товар.
        В данном методе вычисляются координаты расположения данной ячейки
        на схеме всего помещения
        Args:
            cell_index: индекс ячейки на полке, на которой располагается товар
        """
        # обрабатываем ситуацию когда выбрана первая или последня ячейка
        if cell_index == 1:
            return self.x1, self.y1
        elif cell_index == self.cell_count:
            return self.x2, self.y2
        else:
            # вычисляем координатную разницу по ОСИ X
            if self.x1 > self.x2:
                diff_x = self.x1 - self.x2
            else:
                diff_x = self.x2 - self.x1
            # вычисляем координатную разницу по ОСИ Y
            if self.y1 > self.y2:
                diff_y = self.y1 - self.y2
            else:
                diff_y = self.y2 - self.y1
            # вычисляем от отступ который нужно добавить по ОСЯМ чтобы вычислить координаты
            ident_x = diff_x // (self.cell_count - 1) * (cell_index - 1)
            ident_y = diff_y // (self.cell_count - 1) * (cell_index - 1)
            # добавляем отступ к начальной координате каждой из осей, чтобы вычислить координаты ячейки
            # по ОСИ X
            if self.x1 > self.x2:
                cell_x = self.x1 - ident_x
            else:
                cell_x = self.x1 + ident_x
            # по ОСИ Y
            if self.y1 > self.y2:
                cell_y = self.y1 - ident_y
            else:
                cell_y = self.y1 + ident_y
            return cell_x, cell_y


class Painter:
    """Класс с бизнес логикой рисования точек на изображениях.
    Рисунок является планом магазина/склада на котором расставлены
    полки и т.п.
    При помощи данного класса на данных схемах будут отмечаться места
    расположения товаров
    """
    def __init__(self, image_path: str):
        """Инициализация объекта класса"""
        self.image = Image.open(image_path)     # объект изображения
        self.draw = ImageDraw.Draw(self.image)  # объект массива точек изображения с которым будет вестись работа
        try:
            self.font = ImageFont.truetype("arial.ttf", 20)
        except:
            self.font = ImageFont.load_default()

    def add_point(self, x, y, color='red', radius=5, label: str = "", label_offset: int = 5):
        """Добавляет точку на изображение по указанным координатам
        Args:
            x: координата X
            y: координата Y
            color: цвет точки (по умолчанию 'red')
            radius: радиус точки (по умолчанию 5)
            label: цифра которую нужно нарисовать над точкой
            label_offset: отступ цифры от круга
        """
        # Рисуем точку (на самом деле маленький круг)
        bounding_box = [(x - radius, y - radius), (x + radius, y + radius)]
        self.draw.ellipse(bounding_box, fill=color)

        # Если передан label (текст/цифра), рисуем его над точкой
        if label:
            # Получаем размер текста через textbbox
            bbox = self.draw.textbbox((0, 0), str(label), font=self.font)
            text_width = bbox[2] - bbox[0]  # ширина текста
            text_height = bbox[3] - bbox[1]  # высота текста

            # Вычисляем позицию текста (центрируем над точкой)
            text_x = x - text_width // 2
            text_y = y - radius - text_height - label_offset  # Увеличиваем отступ

            self.draw.text((text_x, text_y), str(label), fill=color, font=self.font)

    def save_image(self, output_path):
        """
        Сохраняет изображение с точками по указанному пути
        Args:
            output_path: путь для сохранения
        """
        # Создаем папку, если она не существует
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.image.save(output_path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s")

    # координаты первой полки


    obj = Painter("/home/udalov/python/freelans/where_is_it/core_app/images/shefl_test.jpg")

    shelf = Shelf(
        x1=117,
        y1=395,
        x2=117,
        y2=95,
        cell_count=6
    )

    x, y = shelf.find_coord(cell_index=6)

    print(x, y)


    obj.add_point(x=x, y=y, label="1", radius=4)
    obj.save_image(output_path="/home/udalov/python/freelans/where_is_it/core_app/images/shefl_test_toint.jpg")

