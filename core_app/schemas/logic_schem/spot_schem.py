"""core_app/schemas/logic_schem/spot_shem
В данном модуле находятся схемы, относящиеся к бизнес логике
"""
from typing import List, Optional, Dict

from pydantic import BaseModel

from schemas import storage_schem


class ItemsListSchem(BaseModel):
    """Схема для валидации когда отравляется запрос на поиск
    расположения товаров по ячейкам
    """
    id: int
    name: str


class ItemsIDsSchem(BaseModel):
    ids: List[int]


class SpotResultSchem(BaseModel):
    """Модель которая является результатом отметки ячеек
    расположения товаров
    """
    spots_data: List[storage_schem.spots_schem.SpotsWithShelvesSchem]
    download_url: str


class AddClientSchem(BaseModel):
    name: str
    frontend_service_id: int
    frontend_id: int
    frontend_data: Optional[Dict] = None
