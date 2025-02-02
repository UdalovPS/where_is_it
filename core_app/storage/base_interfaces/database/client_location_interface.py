from abc import ABC, abstractmethod
from typing import Any


class BaseClientLocation(ABC):
    """Интерфейс класс хранящий данные о локации клиента"""
    @abstractmethod
    async def get_client_location(self, client_id: int) -> Any:
        """Абстрактный интерфейс метод для извлечения данных
        о местонахождении клиента.
        Args:
            client_id: идентификатор клиента
        """
        pass

    @abstractmethod
    async def add_client_location(self, client_id: int, building_id: int) -> Any:
        """Абстрактный интерфейс метод для добавления
        назначения клиенту местонахождения.
        Args:
            client_id: идентификатор клиента
            building_id: идентификатор строения, которое привязывается к клиенту
        """
        pass

    @abstractmethod
    async def update_client_location(self, client_id: int, building_id: int) -> Any:
        """Абстрактный интерфейс метод для обновления
        местоположения клиента.
        Args:
            client_id: идентификатор клиента
            building_id: идентификатор строения, которое привязывается к клиенту
        """
        pass
