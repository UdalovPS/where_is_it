from typing import Generic, Optional, TypeVar, Dict, List
import datetime

from pydantic import BaseModel


# Создаем типовой параметр для Pydantic модели
T = TypeVar("T", bound=BaseModel)


class BaseErrorSchem(BaseModel):
    """Базовая схема по формату которой будут указаны все ошибки
    Attr:
        name: наименование ошибки
        details: подробное описание ошибки
        api: наименование раздела в котором осуществлена ошибка
        status_code: статус код ошибки (для REST интерфейса)
    """
    name: str
    details: Optional[str] = None
    api: str
    status_code: int = 400


class BaseResultSchem(BaseModel, Generic[T]):
    """Базовая схема ответа логических методов
    Attr:
        error: ошибка в ответе, если она есть
        data: данные которые возвращает метод
    """
    success: bool = True
    error: Optional[BaseErrorSchem] = None
    data: Optional[T] = None


class ClientLocationSchem(BaseModel):
    id: int
    branch_id: Optional[int]
    organization_id: int
    created_at: datetime.datetime
    update_at: datetime.datetime


class ClientSchem(BaseModel):
    """Схема для представления данных клиента"""
    id: int
    name: str
    frontend_service_id: int
    frontend_id: int
    frontend_data: Optional[Dict]
    created_at: datetime.datetime
    update_at: datetime.datetime
    location: Optional[ClientLocationSchem] = None


class CountrySchem(BaseModel):
    id: int
    name: str
    organization_id: int


class DistrictSchem(BaseModel):
    id: int
    name: str
    organization_id: int
    country_data: CountrySchem


class CitySchem(BaseModel):
    id: int
    name: str
    organization_id: int
    district_data: DistrictSchem


class BranchSchema(BaseModel):
    id: int
    name: str
    address: str
    city_data: CitySchem
    organization_id: int
    latitude: float
    longitude: float


class LocationSchem(BaseModel):
    id: int
    client_id: int
    organization_id: int
    branch_id: Optional[int]


class SimilarItemsSchem(BaseModel):
    id: int
    name: str
    similarity_score: float
    category: str


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


class SpotResultSchem(BaseModel):
    """Модель которая является результатом отметки ячеек
    расположения товаров
    """
    spots_data: List[SpotsWithShelvesSchem]
    download_url: str