"""logics/spots_logic
Логические объекты для поиска местоположения товаров на полках
"""
import logging

# импортируем логические объекты
from logics.base_logic import BaseLogic

# импортируем глобальные объекты
from exceptions import AuthenticationError
from schemas.base_schemas import BaseResultSchem, NullSchem


logger = logging.getLogger(__name__)


class SpotLogic(BaseLogic):
    """Объект с методами для нахождения местоположения товаров на полках"""

    async def use_get_product_data_by_name(
            self,
            frontend_id: int,
            frontend_service_id: int,
            value: str,
            token: str,
            api: str,
    ) -> BaseResultSchem:
        """НАВИГАЦИОННЫЙ МЕТОД поиска данных по товару по его имени.
        - Проходим аутентификацию по токену
        - находим данные клиента в зависимости от типа фронтенд приложения
        - находим в embbedding хранилище данные товаров по имени
        - проверяем в БД есть ли данные товары в нужном помещении и возвращаем результат
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            value: наименование товара
            token: токен аутентификации
            api: раздел в котором происходит действие
        return:
            BaseResultSchem(
                error: Optional[BaseErrorSchem] - данные об ошибке, если она произошла
                data: Any = данные которые должна вернуть API
            )
        """
        try:
            logger.info(f"Обрабатываю логику поиска товара по имени. frontend_id: {frontend_id}, frontend_service_id: {frontend_service_id}, value: {value}")

            # аутентификация
            await self.check_authenticate(token=token, api=api)

            # получаем данные клиента
            client_data =  await self.client_obj.get_data_by_frontend_id(
                frontend_id=frontend_id, frontend_service_id=frontend_service_id
            )
            logger.info(f"Получены данные клиента: {client_data}")

            # производим поиск товара в embedding хранилище

            # проверяем есть ли в в помещении в котором находится пользователь данные товары


            return BaseResultSchem(data=NullSchem(data="strad"))
        except AuthenticationError as _er:
            logger.error(f"Ошибка авторизации -> {_er}")
            return BaseResultSchem(error=_er.error)

