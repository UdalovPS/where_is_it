"""logics/spots_logic
Логические объекты для поиска местоположения товаров на полках
"""
import logging
from typing import List

import schemas.storage_schem.items
# импортируем логические объекты
from logics.base_logic import BaseLogic

# импортируем глобальные объекты
from exceptions import AuthenticationError
from schemas.base_schemas import BaseResultSchem, NullSchem
import exceptions
from exception_handler import handle_view_exception


logger = logging.getLogger(__name__)


class SpotLogic(BaseLogic):
    """Объект с методами для нахождения местоположения товаров на полках"""

    async def use_get_product_data_by_name(
            self,
            frontend_id: int,
            frontend_service_id: int,
            search_name: str,
            token: str,
            api: str,
    ) -> BaseResultSchem[List[schemas.storage_schem.items.SimilarItemsSchem]]:
        """НАВИГАЦИОННЫЙ МЕТОД поиска данных по товару по его имени.
        - Проходим аутентификацию по токену
        - находим данные клиента в зависимости от типа фронтенд приложения
        - проверяем в БД есть ли данные товары в нужном помещении и возвращаем результат
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            search_name: наименование товара который нужно найти
            token: токен аутентификации
            api: раздел в котором происходит действие
        return:
            BaseResultSchem(
                error: Optional[BaseErrorSchem] - данные об ошибке, если она произошла
                data: Any = данные которые должна вернуть API
            )
        """
        try:
            logger.info(f"Обрабатываю логику поиска товара по имени. frontend_id: {frontend_id}, "
                        f"frontend_service_id: {frontend_service_id}, search_name: {search_name}")

            # аутентификация
            await self.check_authenticate(token=token, api=api)

            # получаем данные клиента
            client_data =  await self.client_obj.get_data_by_frontend_id(
                frontend_id=frontend_id, frontend_service_id=frontend_service_id
            )
            logger.info(f"Получены данные клиента: {client_data}")
            if not client_data:
                # если не найдены данные клиента то вызываем ошибку
                raise exceptions.NotFoundError(item_name="client_data", api=api)
            if not client_data.location:
                # если у клиента нет локации на которой он находится
                raise exceptions.NotFoundError(item_name="client_location", api=api)

            # проверяем есть ли в помещении в котором находится пользователь данные товары
            items_data = await self.items_obj.get_similar_items(
                branch_id=client_data.location.branch_id,
                search_name=search_name,
            )
            if not items_data:
                # ошибка если по данному имени не найден товар
                raise exceptions.NotFoundError(item_name="items_data", api=api)

            return BaseResultSchem[List[schemas.storage_schem.items.SimilarItemsSchem]](data=items_data)
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

