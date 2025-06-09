"""routers/spots
Поиск местонахождения товаров на полках
"""

import logging
from typing import Union, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# импортируем логические объекты
# from logics.base_logic import BaseLogic
from logics.spots_logic import SpotLogic

# импортируем глобальные переменные
from fastapi_core import get_token
from schemas import logic_schem


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/spots", tags=['Spots'])


@router.get("/products")
async def get_product_name(
        frontend_id: int,
        frontend_service_id: int,
        search_name: str,
        token: Union[str, None] = Depends(get_token),
        logic_obj: SpotLogic = Depends(SpotLogic)
):
    """Роут для обработки запроса на поиск продукта по его имени в векторном хранилище
    Args:
        frontend_id: идентификатор клиента из frontend сервиса который обращается к API
        frontend_service_id: тип frontend сервиса который взаимодействует с системой
        search_name: имя по которому нужно найти товар
        token: токен авторизации которые передается в заголовке запроса
        logic_obj: логический объект в котором происходит обработки бизнес логики
    """
    logger.info(f"Пришел запрос на определение данных товаров по имени: {search_name}. frontend_id: {frontend_id}, frontend_service_id: {frontend_service_id}")
    res = await logic_obj.use_get_product_data_by_name(
        token=token,
        api="spot/products",
        search_name=search_name,
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id
    )
    # проверяем не произошла ли ошибка
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())


@router.post("/")
async def get_spots(
        frontend_id: int,
        frontend_service_id: int,
        items_ids: logic_schem.spot_schem.ItemsIDsSchem,
        route: bool = False,
        token: Union[str, None] = Depends(get_token),
        logic_obj: SpotLogic = Depends(SpotLogic),
        branch_id: Optional[int] = None
):
    logger.info(f"Пришел запрос схему расположения ячеек в магазине. frontend_id: {frontend_id}, "
                f"frontend_service_id: {frontend_service_id}, items_ids: {items_ids}, "
                f"branch_id: {branch_id}")
    res = await logic_obj.get_spots_schem(
        token=token,
        api="spot/schemas",
        items_ids=items_ids.ids,
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        branch_id=branch_id,
        route=route
    )
    # проверяем не произошла ли ошибка
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())