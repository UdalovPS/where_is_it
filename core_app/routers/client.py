"""routers/spots
Поиск местонахождения товаров на полках
"""

import logging
from typing import Union, Optional
import io

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# импортируем логические объекты
from logics.client_logic import ClientLogic

# импортируем глобальные переменные
from fastapi_core import get_token
from schemas import logic_schem
from schemas.base_schemas import BaseResultSchem


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/client", tags=['Client Router'])


@router.get("/branches/geo")
async def get_product_name(
        frontend_id: int,
        frontend_service_id: int,
        latitude: float,
        longitude: float,
        limit: int = 3,
        token: Union[str, None] = Depends(get_token),
        logic_obj: ClientLogic = Depends(ClientLogic)
):
    """Роут для поиска ближайших филиалов по геолокации
    """
    logger.info(f"Пришел запрос на поиск ближайших филиалов по геолокации. frontend_id: {frontend_id}, "
                f"frontend_service_id: {frontend_service_id}, latitude: {latitude}, "
                f"longitude: {longitude}, limit: {limit}")
    res = await logic_obj.get_branches_by_geo(
        token=token,
        api="client/branches/geo",
        latitude=latitude,
        longitude=longitude,
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        limit=limit
    )
    # проверяем не произошла ли ошибка
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())

@router.patch("/location")
async def update_client_location(
        frontend_id: int,
        frontend_service_id: int,
        branch_id: int,
        token: str,
        logic_obj: ClientLogic = Depends(ClientLogic)
):
    """Обновляем данные локации клиента"""
    res = await logic_obj.update_client_location(
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        branch_id=branch_id,
        token=token,
        api="client/location"
    )
    # проверяем не произошла ли ошибка
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())

@router.get("/countries")
async def get_countries(
        frontend_id: int,
        frontend_service_id: int,
        token: str,
        logic_obj: ClientLogic = Depends(ClientLogic)
):
    """Извлечение списка стран относящихся к определенной организации"""
    res = await logic_obj.get_countries(
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        token=token,
        api="client/counties"
    )
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())

@router.get("/districts")
async def get_districts(
        frontend_id: int,
        frontend_service_id: int,
        search_name: str,
        country_id: int,
        token: str,
        limit: int = 3,
        similarity_threshold: float = 0.1,
        logic_obj: ClientLogic = Depends(ClientLogic)
):
    """Извлечение списка регионов по имени"""
    res = await logic_obj.get_districts_by_name(
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        search_name=search_name,
        country_id=country_id,
        limit=limit,
        similarity_threshold=similarity_threshold,
        token=token,
        api="client/districts"
    )
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())

@router.get("/cities")
async def get_cities(
        frontend_id: int,
        frontend_service_id: int,
        search_name: str,
        district_id: int,
        token: str,
        limit: int = 3,
        similarity_threshold: float = 0.1,
        logic_obj: ClientLogic = Depends(ClientLogic)
):
    """Извлечение списка городов по имени"""
    res = await logic_obj.get_city_by_name(
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        search_name=search_name,
        district_id=district_id,
        limit=limit,
        similarity_threshold=similarity_threshold,
        token=token,
        api="client/cities"
    )
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())

@router.get("/branches")
async def get_cities(
        frontend_id: int,
        frontend_service_id: int,
        search_address: str,
        city_id: int,
        token: str,
        limit: int = 3,
        similarity_threshold: float = 0.1,
        logic_obj: ClientLogic = Depends(ClientLogic)
):
    """Извлечение списка городов по имени"""
    res = await logic_obj.get_branches_by_name(
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        search_address=search_address,
        city_id=city_id,
        limit=limit,
        similarity_threshold=similarity_threshold,
        token=token,
        api="client/branches"
    )
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())

@router.get("/")
async def get_client_data(
        frontend_id: int,
        frontend_service_id: int,
        token: str,
        logic_obj: ClientLogic = Depends(ClientLogic)
):
    """Извлечение данных клиента"""
    res = await logic_obj.get_client_data(
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        token=token,
        api="client/client_data"
    )
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())

@router.post("/")
async def add_new_client_data(
data: logic_schem.spot_schem.AddClientSchem,
        token: str,
        logic_obj: ClientLogic = Depends(ClientLogic)
):
    """Добавление нового клиента"""
    res = await logic_obj.add_new_client_data(
        frontend_id=data.frontend_id,
        frontend_service_id=data.frontend_service_id,
        name=data.name,
        frontend_data=data.frontend_data,
        token=token,
        api="client/client_data"
    )
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())