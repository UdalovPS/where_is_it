"""logics/client_logic
Модуль с бизнес логикой клиента
"""

import logging
from typing import List, Optional, Dict

from sqlalchemy.util import await_only
from watchfiles import awatch

# импортируем логические объекты
from logics.base_logic import BaseLogic

# импортируем глобальные объекты
from schemas.base_schemas import BaseResultSchem
from schemas import storage_schem
import exceptions
from exception_handler import handle_view_exception


logger = logging.getLogger(__name__)


class ClientLogic(BaseLogic):
    """Объект с методами для нахождения местоположения товаров на полках"""

    async def get_branch_data(
            self,
            frontend_id: int,
            frontend_service_id: int,
            token: str,
            api: str,
            latitude: Optional[float] = None,
            longitude: Optional[float] = None,
            search_address: Optional[str] = None,
            city_id: Optional[int] = None,
            limit: int = 3,
            similarity_threshold: float = 0.1,
    ) -> BaseResultSchem[List[storage_schem.branches_schem.BranchSchema]]:
        """Извлечение данных помещения
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            latitude: широта геолокации поиска пользователя
            longitude: долгота геолокации поиска пользователя
            token: токен аутентификации
            api: раздел в котором происходит действие
            limit: максимальное кол-во извлеченных записей
            search_address: адрес поиска
            city_id: идентификатор города
            similarity_threshold: степень похожести
        """
        try:
            logger.info(f"Обрабатываю логику извлечения помещений."
                        f"frontend_id: {frontend_id}, frontend_service_id: {frontend_service_id}, "
                        f"latitude: {latitude}, longitude: {longitude}, "
                        f"token: {token}, api: {api}, limit: {limit}, search_address: {search_address}, "
                        f"city_id: {city_id}, similarity_threshold: {similarity_threshold}")
            # первичная валидация
            if not (latitude and longitude) and not (search_address and city_id):
                raise exceptions.ValidationError(
                    detail="<latitude> and <longitude> or <search_address> and <city_id> can't be empty",
                    api=api
                )
            # аутентификация
            await self.check_authenticate(token=token, api=api)
            if latitude and longitude:
                return await self.get_branches_by_geo(
                    frontend_id=frontend_id,
                    frontend_service_id=frontend_service_id,
                    latitude=latitude,
                    longitude=longitude,
                    api=api,
                    limit=limit
                )
            else:
                return await self.get_branches_by_name(
                    frontend_id=frontend_id,
                    frontend_service_id=frontend_service_id,
                    search_address=search_address,
                    city_id=city_id,
                    limit=limit,
                    similarity_threshold=similarity_threshold,
                    api=api
                )

        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

    async def get_branches_by_geo(
            self,
            frontend_id: int,
            frontend_service_id: int,
            latitude: float,
            longitude: float,
            api: str,
            limit: int = 3
    ) -> BaseResultSchem[List[storage_schem.branches_schem.BranchSchema]]:
        """Поиск ближайших филиалов по геолокации
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            latitude: широта геолокации поиска пользователя
            longitude: долгота геолокации поиска пользователя
            api: раздел в котором происходит действие
            limit: максимальное кол-во извлеченных записей
        """
        logger.info(f"Обрабатываю логику поиска ближайших филиалов по геолокации. "
                    f"frontend_id: {frontend_id}, frontend_service_id: {frontend_service_id}, "
                    f"latitude: {latitude}, longitude: {longitude}, limit: {limit}")
        if not latitude or not longitude:
            raise exceptions.ValidationError(
                api=api,
                detail="<latitude> or <longitude> can't be empty"
            )

        # поиск ближайших точек
        branches = await self.branches_obj.get_data_by_geo(
            organization_id=self.ORGANIZATION_ID,
            latitude=latitude,
            longitude=longitude,
            limit=limit
        )
        if not branches:
            # ошибка если по данному имени не найден товар
            raise exceptions.NotFoundError(item_name="branches_data", api=api)

        return BaseResultSchem[List[storage_schem.branches_schem.BranchSchema]](data=branches)

    async def update_client_location(
            self,
            frontend_id: int,
            frontend_service_id: int,
            branch_id: int,
            token: str,
            api: str,
    ) -> BaseResultSchem[storage_schem.clients_schem.LocationSchem]:
        """Изменение локации клиента
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            branch_id: идентификатор филиала
            token: токен аутентификации
            api: раздел в котором происходит действие
        """
        try:
            logger.info(f"Обрабатываю логику обновления локации пользователя frontend_id: {frontend_id}, "
                        f"frontend_service_id: {frontend_service_id}, branch_id: {branch_id}")
            # аутентификация
            await self.check_authenticate(token=token, api=api)

            # извлекаем данные помещения
            branch_data = await self.branches_obj.get_branch_data_by_id(node_id=branch_id)
            if branch_data.organization_id != self.ORGANIZATION_ID:
                raise exceptions.AccessError(api=api)
            if not branch_data:
                raise exceptions.NotFoundError(item_name="branch_data", api=api)

            # находим данные клиента
            client_data = await self.client_obj.get_data_by_frontend_id(
                frontend_id=frontend_id,
                frontend_service_id=frontend_service_id,
                organization_id=self.ORGANIZATION_ID
            )
            if not client_data:
                # если не найдены данные клиента то вызываем ошибку
                raise exceptions.NotFoundError(item_name="client_data", api=api)

            if client_data.location:
                location = await self.client_location_obj.update_client_location(
                    client_id=client_data.id, branch_id=branch_id, organization_id=self.ORGANIZATION_ID
                )
            else:
                location = await self.client_location_obj.add_client_location(
                    client_id=client_data.id,
                    branch_id=branch_id,
                    organization_id=self.ORGANIZATION_ID
                )
                if not location:
                    raise exceptions.UpdateLocationError(api=api)
            return BaseResultSchem[storage_schem.clients_schem.LocationSchem](data=location)
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

    async def get_countries(
            self,
            frontend_id: int,
            frontend_service_id: int,
            token: str,
            api: str,
    ) -> BaseResultSchem[List[storage_schem.countries_schem.CountrySchem]]:
        """Извлечение списка стран определенной организации
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            token: токен аутентификации
            api: раздел в котором происходит действие
        """
        try:
            logger.info(f"Обрабатываю логику извлечения списка стран. frontend_id: "
                        f"{frontend_id}, frontend_service_id: {frontend_service_id}")
            # аутентификация
            await self.check_authenticate(token=token, api=api)
            countries = await self.countries_obj.get_countries_by_org(organization_id=self.ORGANIZATION_ID)
            if not countries:
                raise exceptions.NotFoundError(item_name="countries_data", api=api)
            return BaseResultSchem[List[storage_schem.countries_schem.CountrySchem]](data=countries)
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

    async def get_districts_by_name(
            self,
            frontend_id: int,
            frontend_service_id: int,
            search_name: str,
            country_id: int,
            limit: int,
            similarity_threshold: float,
            token: str,
            api: str,
    ) -> BaseResultSchem[List[storage_schem.districts_schem.DistrictSchem]]:
        """Извлечение списка стран определенной организации
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            search_name: наименование региона по которому осуществляется поиск
            country_id: идентификатор страны
            limit: кол-во записей которые нужно извлечь
            similarity_threshold: процент похожести
            token: токен аутентификации
            api: раздел в котором происходит действие
        """
        try:
            logger.info(f"Обрабатываю логику извлечения регионов. frontend_id: "
                        f"{frontend_id}, frontend_service_id: {frontend_service_id}, "
                        f"search_name: {search_name}, country_id: {country_id}, "
                        f"limit: {limit}, similarity_threshold: {similarity_threshold}")
            # аутентификация
            await self.check_authenticate(token=token, api=api)
            districts = await self.district_obj.get_similar_by_org_country_and_name(
                organization_id=self.ORGANIZATION_ID,
                search_name=search_name,
                country_id=country_id,
                limit=limit,
                similarity_threshold=similarity_threshold
            )
            if not districts:
                raise exceptions.NotFoundError(item_name="districts_data", api=api)
            return BaseResultSchem[List[storage_schem.districts_schem.DistrictSchem]](data=districts)
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

    async def get_city_by_name(
            self,
            frontend_id: int,
            frontend_service_id: int,
            search_name: str,
            district_id: int,
            limit: int,
            similarity_threshold: float,
            token: str,
            api: str,
    ) -> BaseResultSchem[List[storage_schem.cities_schem.CitySchem]]:
        """Извлечение списка городов
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            search_name: наименование региона по которому осуществляется поиск
            district_id: идентификатор региона
            limit: кол-во записей которые нужно извлечь
            similarity_threshold: процент похожести
            token: токен аутентификации
            api: раздел в котором происходит действие
        """
        try:
            logger.info(f"Обрабатываю логику извлечения городов. frontend_id: "
                        f"{frontend_id}, frontend_service_id: {frontend_service_id}, "
                        f"search_name: {search_name}, district_id: {district_id}, "
                        f"limit: {limit}, similarity_threshold: {similarity_threshold}")
            # аутентификация
            await self.check_authenticate(token=token, api=api)
            cities = await self.cities_obj.get_similar_by_org_district_and_name(
                organization_id=self.ORGANIZATION_ID,
                search_name=search_name,
                district_id=district_id,
                limit=limit,
                similarity_threshold=similarity_threshold
            )
            if not cities:
                raise exceptions.NotFoundError(item_name="cities_data", api=api)
            return BaseResultSchem[List[storage_schem.cities_schem.CitySchem]](data=cities)
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

    async def get_branches_by_name(
            self,
            frontend_id: int,
            frontend_service_id: int,
            search_address: str,
            city_id: int,
            limit: int,
            similarity_threshold: float,
            api: str,
    ):
        """Извлечение списка адресов
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            search_address: адрес по которому происходит поиск
            city_id: идентификатор города
            limit: кол-во записей которые нужно извлечь
            similarity_threshold: процент похожести
            api: раздел в котором происходит действие
        """
        logger.info(f"Обрабатываю логику извлечения адресов frontend_id: "
                    f"{frontend_id}, frontend_service_id: {frontend_service_id}, "
                    f"search_address: {search_address}, city_id: {city_id}, "
                    f"limit: {limit}, similarity_threshold: {similarity_threshold}")
        # валидация
        if not search_address or not city_id:
            raise exceptions.ValidationError(
                api=api,
                detail="<search_address> or <city_id> can't be empty"
            )


        branches = await self.branches_obj.get_similar_by_org_city_and_address(
            organization_id=self.ORGANIZATION_ID,
            search_address=search_address,
            city_id=city_id,
            limit=limit,
            similarity_threshold=similarity_threshold
        )
        if not branches:
            raise exceptions.NotFoundError(item_name="branches_data", api=api)
        return BaseResultSchem[List[storage_schem.branches_schem.BranchSchema]](data=branches)

    async def get_client_data(
            self,
            frontend_id: int,
            frontend_service_id: int,
            token: str,
            api: str,
    ) -> BaseResultSchem[storage_schem.clients_schem.ClientWithLocationSchem]:
        """Извлечение данных клиента
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            token: токен аутентификации
            api: раздел в котором происходит действие
        """
        try:
            logger.info(f"Обрабатываю логику извлечения данных клиента. "
                        f"frontend_id: {frontend_id}, frontend_service_id: {frontend_service_id}")
            # аутентификация
            await self.check_authenticate(token=token, api=api)
            # получаем данные клиента
            client_data = await self.client_obj.get_data_by_frontend_id(
                frontend_id=frontend_id,
                frontend_service_id=frontend_service_id,
                organization_id=self.ORGANIZATION_ID
            )
            if not client_data:
                # если не найдены данные клиента то вызываем ошибку
                raise exceptions.NotFoundError(item_name="client_data", api=api)
            return BaseResultSchem[storage_schem.clients_schem.ClientWithLocationSchem](data=client_data)
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

    async def add_new_client_data(
            self,
            frontend_id: int,
            frontend_service_id: int,
            name: str,
            token: str,
            api: str,
            frontend_data: Optional[Dict] = None,
    ) -> BaseResultSchem[storage_schem.clients_schem.ClientWithLocationSchem]:
        """Добавления нового клиента в БД
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            name: имя клиента
            token: токен аутентификации
            api: раздел в котором происходит действие
            frontend_data: данные клиента персональный для каждого типа мессенджера
        """
        try:
            # аутентификация
            await self.check_authenticate(token=token, api=api)

            new_client = await self.client_obj.add_new_client(
                name=name,
                frontend_service_id=frontend_service_id,
                frontend_id=frontend_id,
                frontend_data=frontend_data
            )
            if not new_client:
                raise exceptions.AddError(api=api, item="client_data")
            return BaseResultSchem[storage_schem.clients_schem.ClientWithLocationSchem](data=new_client)
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)