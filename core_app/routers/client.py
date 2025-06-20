"""routers/client
Ручки которыми пользуется рядовой клиент
"""

import logging
from typing import Union, Optional, List
import io

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, StreamingResponse

# импортируем логические объекты
from logics.client_logic import ClientLogic
from logics.spots_logic import SpotLogic

# импортируем глобальные переменные
from fastapi_core import get_token
from schemas import logic_schem, storage_schem
from schemas.base_schemas import BaseResultSchem


logger = logging.getLogger(__name__)

FRONTEND_ID = Query(..., description="Идентификатор клиента во внешней системе")
FRONTEND_SERVICE_ID = Query(..., description="Идентификатор внешней системы клиента")
BRANCH_ID = Query(..., description="Идентификатор помещения")
SEARCH_NAME = Query(..., description="Наименование по которому осуществляется поиск")
LIMIT = Query(10, description="Максимальное кол-во записей которое необходимо вернуть в ответ на запрос")
THRESHOLD = Query(0.1, description="Степень сходства искомого значения и результата (от 0.1 до 1)", ge=0.1, le=1.0)

router = APIRouter(prefix="/client", tags=['Client Router'])


@router.get(
    "",
    response_model=BaseResultSchem[storage_schem.clients_schem.ClientWithLocationSchem],
    summary="Извлечение данных клиента",
    description="Извлечения данных клиента",
    response_description="Данные клиента"
)
async def get_client_data(
        frontend_id: int = FRONTEND_ID,
        frontend_service_id: int = FRONTEND_SERVICE_ID,
        token: Union[str, None] = Depends(get_token),
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


@router.post(
    "",
    response_model=BaseResultSchem[storage_schem.clients_schem.ClientWithLocationSchem],
    summary="Добавление нового клиента",
    description="name: Имя клиента frontend_service_id: Идентификатор внешней системы клиента "
                "frontend_id: Идентификатор клиента во внешней системе "
                "frontend_data: Дополнительные данные клиента (необязательно)",
    response_description="Данные клиента"
)
async def create_new_client(
        data: logic_schem.spot_schem.AddClientSchem,
        token: Union[str, None] = Depends(get_token),
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


@router.patch(
    "/location",
    response_model=BaseResultSchem[storage_schem.clients_schem.LocationSchem],
    summary="Обновления локации клиента",
    description="Обновление локации клиента (помещения в котором будет производиться поиск товаров)",
    response_description="Данные локации клиента"
)
async def update_client_location(
        frontend_id: int = FRONTEND_ID,
        frontend_service_id: int = FRONTEND_SERVICE_ID,
        branch_id: int = BRANCH_ID,
        token: Union[str, None] = Depends(get_token),
        logic_obj: ClientLogic = Depends(ClientLogic)
):
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


@router.get(
    "/countries",
    response_model=BaseResultSchem[List[storage_schem.countries_schem.CountrySchem]],
    summary="Извлечение списка стран",
    description="Извлечения списка стран, которые доступны данному клиенту для выбора локации",
    response_description="Список стран"
)
async def get_countries(
        frontend_id: int = FRONTEND_ID,
        frontend_service_id: int = FRONTEND_SERVICE_ID,
        token: Union[str, None] = Depends(get_token),
        logic_obj: ClientLogic = Depends(ClientLogic)
):
    """Извлечение списка стран относящихся к определенной организации"""
    res = await logic_obj.get_countries(
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        token=token,
        api="client/countries"
    )
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())


@router.get(
    "/districts",
    response_model=BaseResultSchem[List[storage_schem.districts_schem.DistrictSchem]],
    summary="Извлечения списка регионов",
    description="Извлечение списка наиболее похожих на search_name регионов определенной страны",
    response_description="Список регионов"
)
async def get_districts(
        frontend_id: int = FRONTEND_ID,
        frontend_service_id: int = FRONTEND_SERVICE_ID,
        search_name: str = SEARCH_NAME,
        country_id: int = Query(..., description="Идентификатор страны"),
        token: Union[str, None] = Depends(get_token),
        limit: int = LIMIT,
        similarity_threshold: float = THRESHOLD,
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


@router.get(
    "/cities",
    response_model=BaseResultSchem[List[storage_schem.cities_schem.CitySchem]],
    summary="Извлечения списка городов",
    description="Извлечение списка наиболее похожих на search_name городов определенного региона",
    response_description="Список городов"
)
async def get_cities(
        frontend_id: int = FRONTEND_ID,
        frontend_service_id: int = FRONTEND_SERVICE_ID,
        search_name: str = SEARCH_NAME,
        district_id: int = Query(..., description="Идентификатор региона"),
        token: Union[str, None] = Depends(get_token),
        limit: int = LIMIT,
        similarity_threshold: float = THRESHOLD,
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


@router.get(
    "/branches",
    response_model=BaseResultSchem[List[storage_schem.branches_schem.BranchSchema]],
    summary="Извлечения данных помещения",
    description="Извлечение данных помещения по геолокации или по городу и адресу",
    response_description="Данный помещения"
)
async def get_branches(
        frontend_id: int = FRONTEND_ID,
        frontend_service_id: int = FRONTEND_SERVICE_ID,
        search_address: Optional[str] = Query(None, description="Адрес поиска (необязательно если указана геолокация)"),
        city_id: Optional[int] = Query(None, description="Идентификатор города (необязательно если указана геолокация"),
        latitude: Optional[float] = Query(None, description="Широта (необязательно если указан адрес и город"),
        longitude: Optional[float] = Query(None, description="Широта (необязательно если указан адрес и город"),
        token: Union[str, None] = Depends(get_token),
        limit: int = LIMIT,
        similarity_threshold: float = THRESHOLD,
        logic_obj: ClientLogic = Depends(ClientLogic)
):
    """Извлечение списка городов по имени"""
    res = await logic_obj.get_branch_data(
        frontend_id=frontend_id,
        frontend_service_id=frontend_service_id,
        search_address=search_address,
        city_id=city_id,
        limit=limit,
        similarity_threshold=similarity_threshold,
        token=token,
        api="client/branches",
        longitude=longitude,
        latitude=latitude
    )
    if res.error:
        return JSONResponse(status_code=res.error.status_code, content=res.model_dump())
    else:
        return JSONResponse(status_code=200, content=res.model_dump())


@router.get(
    "/items",
    response_model=BaseResultSchem[List[storage_schem.items_schem.SimilarItemsSchem]],
    summary="Извлечения списка товаров",
    description="Извлечение списка товаров в помещении с локацией за которой закреплен клиент или"
                "в указанном branch_id с наиболее похожим наименованием",
    response_description="Данные продуктов с наиболее похожим наименованием расположенные в помещении"
)
async def get_product_name(
        search_name: str = SEARCH_NAME,
        limit: int = LIMIT,
        similarity_threshold: float = THRESHOLD,
        token: Union[str, None] = Depends(get_token),
        logic_obj: SpotLogic = Depends(SpotLogic),
        frontend_id: Optional[int] = Query(None, description="Идентификатор клиента во внешней системе (необязательно если указан branch_id)"),
        frontend_service_id: Optional[int] = Query(None, description="Идентификатор внешней системы клиента (необязательно если указан branch_id)"),
        branch_id: Optional[int] = Query(None, description="Идентификатор помещения (не обязательно если указаны frontend данные)")
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


@router.post(
    "/spots",
    response_model=BaseResultSchem[logic_schem.spot_schem.SpotResultSchem],
    summary="Данные ячеек с товарами",
    description="Извлечь список ячеек (с координатами на схеме помещения) "
                "на которых расположены товары из списка items_ids и ссылку "
                "на скачивание схемы с нанесенными на ней координатами точек",
    response_description="Список ячеек"

)
async def get_spots(
        items_ids: logic_schem.spot_schem.ItemsIDsSchem,
        route: bool = Query(False, description="Флаг true - необходимо построить оптимальный маршрут"
                                               " нахождения всех товаров"),
        token: Union[str, None] = Depends(get_token),
        logic_obj: SpotLogic = Depends(SpotLogic),
        frontend_id: Optional[int] = Query(None,
                                           description="Идентификатор клиента во внешней системе (необязательно если указан branch_id)"),
        frontend_service_id: Optional[int] = Query(None,
                                                   description="Идентификатор внешней системы клиента (необязательно если указан branch_id)"),
        branch_id: Optional[int] = Query(None,
                                         description="Идентификатор помещения (не обязательно если указаны frontend данные)")
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


@router.get(
    "/download/{key}",
    summary="Скачать схему помещения",
    description="Скачать схему помещения с нанесенными на ней координатами ячеек"
)
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