import logging
from typing import Optional, Union, List
from io import BytesIO

import httpx

from config import WEB_URL, WEB_TOKEN, FRONTEND_SERVICE_ID
import schemas

logger = logging.getLogger(__name__)


class WebCore:
    headers = {
        'Content-Type': 'application/json',
        "auth-token": WEB_TOKEN
    }

    """Класс для взаимодействия с web сервисом по API"""
    async def base_request(
            self,
            method: str,
            sub_url: str,
            body: Union[dict, list, None] = None,
            params: Optional[dict] = None,
            timeout: Optional[float] = None
    ) -> dict:
        """Базовый метод http запроса к web серверу
        Args:
            method: http метод
            sub_url: добавочный адрес к базовому, по которому нужно отправить запрос
            body: тело запроса
            params: параметры запроса
            timeout: таймаут запроса в секундах
        """
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response: httpx.Response = await client.request(
                    method=method,
                    url=WEB_URL + sub_url,
                    json=body,
                    params=params,
                    headers=self.headers,
                    timeout=timeout
                )
                logger.info(f"result: {response.json()}")
                return response.json()
            except Exception as _ex:
                logger.error(f"Ошибка при отправке запроса. {method}, {sub_url}, {body}, {params} -> {_ex}")
                return {"success": False, "data": None, "error": None}

    async def base_images_request(
            self,
            method: str,
            url: str,
            body: Union[dict, list, None] = None,
            params: Optional[dict] = None,
            timeout: Optional[float] = None
    ) -> Union[dict, BytesIO]:
        """Базовый метод http запроса к web серверу для выгрузки изображения
        Args:
            method: http метод
            url: url на который требуется отправить запрос
            body: тело запроса
            params: параметры запроса
            timeout: таймаут запроса в секундах
        """
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response: httpx.Response = await client.request(
                    method=method,
                    url=url,
                    json=body,
                    params=params,
                    headers=self.headers,
                    timeout=timeout
                )

                if 'image/jpeg' not in response.headers.get('Content-Type', ''):
                    logger.error("Ошибка. Ответ не является изображением")
                    return response.json()

                image_file = BytesIO(response.content)
                image_file.name = 'image.jpg'  # Имя файла для Telegram
                return image_file
            except Exception as _ex:
                logger.error(f"Ошибка при запросе файла {url} -> {_ex}")
                return {"success": False, "data": None, "error": None}

    async def get_web_user_data(self, user_id: int) -> schemas.BaseResultSchem[schemas.ClientSchem]:
        """Запрос данных пользователя из web приложения
        Args:
            user_id: идентификатор пользователя (from_user.id из телеграм)
        """
        logger.info(f"Запрашиваю данные пользователя: {user_id}")
        response = await self.base_request(
            method="GET",
            sub_url="client",
            params={"frontend_id": user_id, "frontend_service_id": FRONTEND_SERVICE_ID}
        )
        return schemas.BaseResultSchem[schemas.ClientSchem].model_validate(response)

    async def create_new_user(
            self,
            user_id: int,
            name: str,
            username: Optional[str] = None
    ) -> schemas.BaseResultSchem[schemas.ClientSchem]:
        """Создаем нового пользователя в БД web приложения
        Args:
            user_id: идентификатор пользователя
            name: имя пользователя
            username: username пользователя из телеграм
        """
        logger.info(f"Создаю нового пользователя user_id: {user_id}, name: {name}, username: {username}")
        response = await self.base_request(
            method="POST",
            sub_url="client",
            body={
                "name": name,
                "frontend_service_id": FRONTEND_SERVICE_ID,
                "frontend_id": user_id,
                "frontend_data": {
                    "username": username
                }
            }
        )
        return schemas.BaseResultSchem[schemas.ClientSchem].model_validate(response)

    async def get_location_by_geo(
            self,
            latitude: float,
            longitude: float,
            user_id: int,
            limit: int = 3
    ) -> schemas.BaseResultSchem[List[schemas.BranchSchema]]:
        """Извлекаем данные филиалов наиболее близких к текущей геолокации
        Args:
            latitude: широта
            longitude: долгота
            user_id: идентификатор пользователя
            limit: кол-во записей которые нужно вернуть
        """
        logger.info(f"Запрашиваю список филиалов для user: {user_id} по геолокации: {latitude}:{longitude}")
        response = await self.base_request(
            method="GET",
            sub_url="client/branches/geo",
            params={
                "frontend_service_id": FRONTEND_SERVICE_ID,
                "frontend_id": user_id,
                "latitude": latitude,
                "longitude": longitude,
                "limit": limit
            }
        )
        return schemas.BaseResultSchem[List[schemas.BranchSchema]].model_validate(response)

    async def update_client_location(
            self,
            branch_id: int,
            user_id: int
    ) -> schemas.BaseResultSchem[schemas.LocationSchem]:
        """Обновляем локацию клиента
        Args:
            branch_id: идентификатор филиала
            user_id: идентификатор пользователя
        """
        logger.info(f"Изменяю локацию клиента: {user_id} на {branch_id}")
        response = await self.base_request(
            method="PATCH",
            sub_url="client/location",
            params={
                "frontend_service_id": FRONTEND_SERVICE_ID,
                "frontend_id": user_id,
                "branch_id": branch_id,
            }
        )
        return schemas.BaseResultSchem[schemas.LocationSchem].model_validate(response)

    async def get_countries(self, user_id: int) -> schemas.BaseResultSchem[List[schemas.CountrySchem]]:
        """Запрос списка стран"""
        logger.info(f"Запрашиваю список стран относящихся к user: {user_id}")
        response = await self.base_request(
            method="GET",
            sub_url="client/countries",
            params={
                "frontend_service_id": FRONTEND_SERVICE_ID,
                "frontend_id": user_id,
            }
        )
        return schemas.BaseResultSchem[List[schemas.CountrySchem]].model_validate(response)

    async def get_districts_by_name(
            self,
            country_id: int,
            search_name: str,
            user_id: int,
            limit: int = 3,
            similarity_threshold: float = 0.1
    ) -> schemas.BaseResultSchem[List[schemas.DistrictSchem]]:
        """Извлечения регионов по стране и наименованию
        Args:
            country_id: идентификатор страны
            search_name: наименование региона, который необходимо найти
            user_id: идентификатор пользователя из telegram
            limit: кол-во возвращаемых записей
            similarity_threshold: доля похожести введенного значения
        """
        logger.info(f"Запрашиваю список регионов страны: {country_id} -{search_name}")
        response = await self.base_request(
            method="GET",
            sub_url="client/districts",
            params={
                "frontend_service_id": FRONTEND_SERVICE_ID,
                "frontend_id": user_id,
                "search_name": search_name,
                "country_id": country_id,
                "limit": limit,
                "similarity_threshold": similarity_threshold,
            }
        )
        return schemas.BaseResultSchem[List[schemas.DistrictSchem]].model_validate(response)

    async def get_city_by_name(
            self,
            district_id: int,
            search_name: str,
            user_id: int,
            limit: int = 3,
            similarity_threshold: float = 0.1
    ) -> schemas.BaseResultSchem[List[schemas.CitySchem]]:
        """Извлечения регионов по стране и наименованию
        Args:
            district_id: идентификатор региона
            search_name: наименование региона, который необходимо найти
            user_id: идентификатор пользователя из telegram
            limit: кол-во возвращаемых записей
            similarity_threshold: доля похожести введенного значения
        """
        logger.info(f"Запрашиваю список городов: {district_id} -{search_name}")
        response = await self.base_request(
            method="GET",
            sub_url="client/cities",
            params={
                "frontend_service_id": FRONTEND_SERVICE_ID,
                "frontend_id": user_id,
                "search_name": search_name,
                "district_id": district_id,
                "limit": limit,
                "similarity_threshold": similarity_threshold,
            }
        )
        return schemas.BaseResultSchem[List[schemas.CitySchem]].model_validate(response)

    async def get_branches_by_address(
            self,
            city_id: int,
            search_name: str,
            user_id: int,
            limit: int = 3,
            similarity_threshold: float = 0.1
    ) -> schemas.BaseResultSchem[List[schemas.BranchSchema]]:
        """Извлечения регионов по стране и наименованию
        Args:
            city_id: идентификатор города
            search_name: наименование региона, который необходимо найти
            user_id: идентификатор пользователя из telegram
            limit: кол-во возвращаемых записей
            similarity_threshold: доля похожести введенного значения
        """
        logger.info(f"Запрашиваю список адресов: {city_id} -{search_name}")
        response = await self.base_request(
            method="GET",
            sub_url="client/branches",
            params={
                "frontend_service_id": FRONTEND_SERVICE_ID,
                "frontend_id": user_id,
                "search_address": search_name,
                "city_id": city_id,
                "limit": limit,
                "similarity_threshold": similarity_threshold,
            }
        )
        return schemas.BaseResultSchem[List[schemas.BranchSchema]].model_validate(response)

    async def get_items_by_name(
            self,
            search_name: str,
            user_id: int,
            limit: int = 3,
            similarity_threshold: float = 0.1
    ) -> schemas.BaseResultSchem[List[schemas.SimilarItemsSchem]]:
        """Извлечения регионов по стране и наименованию
        Args:
            search_name: наименование региона, который необходимо найти
            user_id: идентификатор пользователя из telegram
            limit: кол-во возвращаемых записей
            similarity_threshold: доля похожести введенного значения
        """
        logger.info(f"Запрашиваю список товаров похожих по имени: {search_name}")
        response = await self.base_request(
            method="GET",
            sub_url="spots/products",
            params={
                "frontend_service_id": FRONTEND_SERVICE_ID,
                "frontend_id": user_id,
                "search_name": search_name,
                "limit": limit,
                "similarity_threshold": similarity_threshold,
            }
        )
        return schemas.BaseResultSchem[List[schemas.SimilarItemsSchem]].model_validate(response)

    async def get_spots_by_items(
            self,
            items_ids: List[int],
            user_id: int,
    ) -> schemas.BaseResultSchem[schemas.SpotResultSchem]:
        """Извлечение слотов и координат их положения на схеме магазина
        Args:
            items_ids: список идентификаторов товаров
            user_id: идентификатор пользователя
        """
        logger.info(f"Запрашиваю схему товаров по списку: {items_ids}, {user_id}")
        response = await self.base_request(
            method="POST",
            sub_url="spots",
            params={
                "frontend_service_id": FRONTEND_SERVICE_ID,
                "frontend_id": user_id,
                "route": True,
            },
            body={"ids": items_ids}
        )
        return schemas.BaseResultSchem[schemas.SpotResultSchem].model_validate(response)

    async def download_scheme(self, url: str) -> Union[dict, BytesIO]:
        """Скачиваем схему размещения товаров на полках по
        специальной ссылке, которая была сгенерирована для скачивания
        Args:
            url: ссылка по которой нужно скачать схему
        """
        logger.info(f"Выгружаю изображение по url: {url}")
        return await self.base_images_request(url=url, method="GET")
