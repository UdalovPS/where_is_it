"""routers/spots
Поиск местонахождения товаров на полках
"""

import logging
from typing import Union, Optional
import io

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse

# импортируем логические объекты
from logics.spots_logic import SpotLogic

# импортируем глобальные переменные
from fastapi_core import get_token
from schemas import logic_schem
from schemas.base_schemas import BaseResultSchem


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/spots", tags=['Spots'])


@router.get("/products")
async def get_product_name(
        search_name: str,
        limit: int = 3,
        similarity_threshold: float = 0.1,
        token: Union[str, None] = Depends(get_token),
        logic_obj: SpotLogic = Depends(SpotLogic),
        frontend_id: Optional[int] = None,
        frontend_service_id: Optional[int] = None,
        branch_id: Optional[int] = None
):
    """Роут для обработки запроса на поиск продукта по его имени в векторном хранилище
    Args:
        frontend_id: идентификатор клиента из frontend сервиса который обращается к API
        frontend_service_id: тип frontend сервиса который взаимодействует с системой
        search_name: имя по которому нужно найти товар
        limit: кол-во записей который нужно извлечь
        similarity_threshold: степень похожести
        token: токен авторизации которые передается в заголовке запроса
        logic_obj: логический объект в котором происходит обработки бизнес логики
        branch_id: идентификатор помещения в котором необходимо найти товары
    """
    logger.info(f"Пришел запрос на определение данных товаров по имени: {search_name}. frontend_id: {frontend_id}, frontend_service_id: {frontend_service_id}")
    res = await logic_obj.use_get_product_data_by_name(
        token=token,
        api="spot/products",
        search_name=search_name,
        limit=limit,
        similarity_threshold=similarity_threshold,
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        branch_id=branch_id
    )
    # проверяем не произошла ли ошибка
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())


@router.post("/")
async def get_spots(
        items_ids: logic_schem.spot_schem.ItemsIDsSchem,
        route: bool = False,
        token: Union[str, None] = Depends(get_token),
        logic_obj: SpotLogic = Depends(SpotLogic),
        frontend_id: Optional[int] = None,
        frontend_service_id: Optional[int] = None,
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


@router.get("/download/{key}")
async def download_schem(
        key: str,
        token: Union[str, None] = Depends(get_token),
        logic_obj: SpotLogic = Depends(SpotLogic),
):
    """Выгружаем файл с картинкой на которой отмечены ячейки
    Args:
        key: ключ для скачивания файла
        token: токен авторизации которые передается в заголовке запроса
        logic_obj: логический объект в котором происходит обработки бизнес логики
    """
    res = await logic_obj.download_schem(download_key=key, token=token, api="spot/download")

    if isinstance(res, BaseResultSchem):
        if res.error:
            return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
        else:
            return JSONResponse(status_code=200, content=res.model_dump())

    else:
        # обрабатывае логику скачивания файла
        img_byte_arr = io.BytesIO()
        res.save(img_byte_arr, format=res.format)  # Сохраняем в исходном формате
        img_byte_arr.seek(0)  # Перемещаем указатель в начало

        # Возвращаем файл для скачивания
        return StreamingResponse(
            img_byte_arr,
            media_type=f"image/{res.format.lower()}",  # Например, "image/jpeg"
            headers={
                "Content-Disposition": "attachment; filename=schem.jpg"  # Меняем имя файла
            }
        )