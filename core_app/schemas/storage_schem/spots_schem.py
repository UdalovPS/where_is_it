import datetime
from typing import Optional

from pydantic import BaseModel


def convert_datetimes(obj):
    """
    Рекурсивно преобразует объекты datetime в ISO-строки.
    Если встречается вложенная модель (наследник BaseModel), пытаемся вызвать ее метод model_dump.
    """
    from pydantic import BaseModel

    if isinstance(obj, BaseModel):
        # Если у вложенной модели есть переопределенный model_dump, используем его
        if hasattr(obj, "model_dump"):
            return convert_datetimes(obj.model_dump())
        else:
            return convert_datetimes(obj.dict())
    elif isinstance(obj, dict):
        return {k: convert_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetimes(item) for item in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj


class SpotSchem(BaseModel):
    id: int
    organization_id: int
    cell_number: int
    floor_number: int
    x_spot_coord: Optional[int] = None
    y_spot_coord: Optional[int] = None


class ShelfSchem(BaseModel):
    id: int
    name: str
    branch_id: int
    organization_id: int
    x1: int
    y1: int
    x2: int
    y2: int
    cell_count: int
    floor_count: int


class ItemDataSchem(BaseModel):
    id: int
    name: str


class SpotsWithShelvesSchem(SpotSchem):
    shelf_data: ShelfSchem
    item_data: ItemDataSchem

    def model_dump(self, *args, **kwargs) -> dict:
        # Получаем «сырые» данные модели
        raw_data = super().model_dump(*args, **kwargs)
        # Преобразуем datetime в ISO-строки
        return convert_datetimes(raw_data)