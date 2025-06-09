"""core_app/schemas/logic_schem/spot_shem
В данном модуле находятся схемы, относящиеся к бизнес логике
"""
from typing import List, Optional

from pydantic import BaseModel


class ItemsListSchem(BaseModel):
    """Схема для валидации когда отравляется запрос на поиск
    расположения товаров по ячейкам
    """
    id: int
    name: str


class ItemsIDsSchem(BaseModel):
    ids: List[int]



