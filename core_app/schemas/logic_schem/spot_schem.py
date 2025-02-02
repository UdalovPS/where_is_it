"""core_app/schemas/logic_schem/spot_shem
В данном модуле находятся схемы, относящиеся к бизнес логике
"""
from typing import List, Optional

from pydantic import BaseModel

# импортируем глобальные переменные
from schemas.base_schemas import BaseResultSchem


# class ProductFlorSchem(BaseModel):
#     """Сущность содержащая информацию
#     о наименовании товара и на каком этаже
#     он находится на полке
#     Attr:
#         product_name: наименование продукта
#         floor: номер этажа на полках
#     """
#     product_name: str
#     floor: int
#
#
# class SpotSchem(BaseModel):
#     """Сущность содержащая информацию
#     о положении товара на полках магазина/склада
#     """
#     latitude: int
#     longitud: int
#     product: List[ProductFlorSchem]
#
#
# class AddrSchem(BaseModel):
#     """Сущность содержащая информации о помещении,
#     на полках которого разложены товары
#     Attr:
#         country_id: идентификатор страны
#         region_id: идентификатор региона уровня областей/штатов
#         city_id: идентификатор города
#         district_id: идентификатор района в городе
#         building_id: идентификатор помещения в котором находится магазин/склад
#     """
#     country_id: int
#     region_id: int
#     city_id: int
#     district_id: int
#     building_id: int
#
#
# class OutProductSpotSchem(BaseModel):
#     """ГЛАВНАЯ ВЫХОДНАЯ сущность которую должна отдать логика
#     product_spot.
#     В данной сущности указано где какой товар лежит на полках
#     Attr:
#         customer_id: идентификатор заказчика
#         location: информация о помещении на полках которого лежит товар
#         spots: информация о том, где и как разложены товары на полках
#     """
#     customer_id: int
#     location: AddrSchem
#     spots: List[SpotSchem]


class ProductSchem(BaseModel):
    id: int
    name: str


class ProductsSchem(BaseResultSchem):
    """Схема с результатом запроса поиска продукта в векторном хранилище"""
    data: Optional[List[ProductSchem]] = None


