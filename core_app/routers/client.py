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