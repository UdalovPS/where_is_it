from typing import Union, Optional
import logging

# импортируем глобальные объекты
from storage.core import StorageCommon
from exceptions import AuthenticationError
from schemas.base_schemas import BaseResultSchem

logger = logging.getLogger(__name__)


class BaseLogic(StorageCommon):
    """Родительский класс для всех объектов выполняющих бизнес логику.
    В данном классе инкапсулированы все общение методы + логика
    взаимодействия с БД и КЭШем
    Attr:
        AUTH_CUSTOMER - переменная определяющая к какому заказчику относится запрос
    """
    def __init__(self):
        self.CUSTOMER_ID: Optional[int] = None

    async def check_authenticate(self, token: Optional[str], api: str):
        """Проверяем аутентификацию по токену доступа
        Args:
            token: токен доступа к АПИ
            api: наименование раздела кода к которому идет обращение
        """
        data = await self.auth_obj.get_data_by_token(token=token)
        if not data:
            logger.error(f"Ошибка аутентификации запроса по токену: {token} API: <{api}>")
            raise AuthenticationError(token=token, api=api)
        else:
            # выставляем переменную которая показывает к какому заказчику относится запрос
            logger.info(f"Запрос по API: <{api}> относится к заказчику: {data.customer_id}")
            self.CUSTOMER_ID = data.customer_id



if __name__ == '__main__':
    pass
