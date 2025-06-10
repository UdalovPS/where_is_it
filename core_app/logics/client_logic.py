"""logics/client_logic
Модуль с бизнес логикой клиента
"""

"""logics/spots_logic
Логические объекты для поиска местоположения товаров на полках
"""
import logging
from typing import List

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

    async def get_branches_by_geo(
            self,
            frontend_id: int,
            frontend_service_id: int,
            latitude: float,
            longitude: float,
            token: str,
            api: str,
            limit: int = 3
    ):
        """Поиск ближайших филиалов по геолокации
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            latitude: широта геолокации поиска пользователя
            longitude: долгота геолокации поиска пользователя
            token: токен аутентификации
            api: раздел в котором происходит действие
            limit: максимальное кол-во извлеченных записей
        """
        try:
            logger.info(f"Обрабатываю логику поиска ближайших филиалов по геолокации. "
                        f"frontend_id: {frontend_id}, frontend_service_id: {frontend_service_id}, "
                        f"latitude: {latitude}, longitude: {longitude}, limit: {limit}")

            # аутентификация
            await self.check_authenticate(token=token, api=api)

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
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

    async def update_client_location(
            self,
            frontend_id: int,
            frontend_service_id: int,
            branch_id: int,
            token: str,
            api: str,
    ):
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

            # находим данные клиента
            client_data = await self.client_obj.get_data_by_frontend_id(frontend_id=frontend_id, frontend_service_id=frontend_service_id)
            if not client_data:
                # если не найдены данные клиента то вызываем ошибку
                raise exceptions.NotFoundError(item_name="client_data", api=api)

            # поиск ближайших точек
            update = await self.client_location_obj.update_client_location(
                client_id=client_data.id, branch_id=branch_id
            )

            return BaseResultSchem[storage_schem.clients_schem.LocationSchem](data=update)
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)