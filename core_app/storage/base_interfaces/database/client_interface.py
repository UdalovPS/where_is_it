from abc import ABC, abstractmethod
from typing import Any, Union

from schemas import storage_schem


class BaseClient(ABC):
    """Интерфейс класс хранящий данные о клиенте"""
    @abstractmethod
    async def add_new_client(
            self,
            messenger_id: int,
            messenger_type: int,
            name: Union[str, None],
            phone: Union[str, None],
            username: Union[str, None],
            age: Union[int, None]
    ) -> storage_schem.ClientSchem:
        """Абстрактный интерфейс метод добавления нового клиента в БД
         Args:
             messenger_id: идентификатор из мессенджера/приложения
             messenger_type: тип мессенджера/приложения
             name: имя клиента (не обязательный параметр)
             phone: номер телефона клиента (не обязательный параметр)
             username: username клиента (не обязательный параметр)
             age: возраст клиента (не обязательный параметр)
        """
        pass

    @abstractmethod
    async def get_client_data_by_messenger_id(
            self,
            messenger_id: int,
            messenger_type: int
    ) -> Union[storage_schem.ClientSchem, None]:
        """Абстрактный интерфейс метод извлекающий данные клиента из БД
        Args:
            messenger_id: идентификатор из мессенджера/приложения
            messenger_type: тип мессенджера/приложения
        """
        pass
