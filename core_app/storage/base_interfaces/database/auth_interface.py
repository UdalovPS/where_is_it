from abc import ABC, abstractmethod
from typing import Union

from schemas import storage_schem


class BaseAuth(ABC):
    """Интерфейс для аутентификации"""
    @abstractmethod
    async def get_data_by_token(self, token: str) -> Union[storage_schem.AuthSchem, None]:
        """Интерфейс метод возвращает данные по токену
        Args:
            token: токен авторизации закрепленный за заказчиком
        """
        pass

    @abstractmethod
    async def update_token(self, node_id: int) -> Union[str, None]:
        """Интерфейс метод обновляет токен по идентификатору записи
        Args:
            node_id: идентификатор записи в БД аутентификации
        """
        pass

    @abstractmethod
    async def add_new_token(self, customer_id: int, name: str) -> Union[storage_schem.AuthSchem, None]:
        """Интерфейс метод создающий новый токен и закрепляющий его за
        заказчиком
        Args:
            customer_id: идентификатор заказчика
            name: название токена (для визуализации и читаемости кода)
        """
        pass
