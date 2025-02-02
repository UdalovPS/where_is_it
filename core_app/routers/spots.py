"""routers/spots
Поиск местонахождения товаров на полках
"""

import logging
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# импортируем логические объекты
# from logics.base_logic import BaseLogic
from logics.spots_logic import SpotLogic

# импортируем глобальные переменные
from fastapi_core import get_token


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/spots", tags=['Spots'])


@router.get("/products")
async def get_product_name(
        client_id: Union[int, str],
        frontend_name: str,
        product_name: str,
        token: Union[str, None] = Depends(get_token)
):
    """Роут для обработки запроса на поиск продукта по его имени в векторном хранилище
    Args:
        client_id: идентификатор клиента в системе мессенджера
        frontend_name: наименование фронтенда из которого приходит ответ (telegram или т.п.)
        product_name: имя по которому нужно найти товар
        token: токен авторизации которые передается в заголовке запроса
        client_id: идентификатор клиента в
    """
    logger.info(f"Пришел запрос на определение данных товаров по имени")
    logic_obj = SpotLogic()
    res = await logic_obj.use_get_product_data_by_name_logic(token=token, api="spot/product", value=product_name)

    # проверяем не произошла ли ошибка
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())
