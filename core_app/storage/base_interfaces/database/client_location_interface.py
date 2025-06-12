from abc import ABC, abstractmethod
from typing import Any, Optional

from schemas import storage_schem


class BaseClientLocation(ABC):
    """Интерфейс класс хранящий данные о локации клиента"""
    @abstractmethod
    async def add_client_location(
            self,
            client_id: int,
            branch_id: Optional[int],
            organization_id: int
    ) -> Optional[storage_schem.clients_schem.LocationSchem]:
        """Абстрактный интерфейс метод для добавления
        назначения клиенту местонахождения.
        Args:
            client_id: идентификатор клиента
            branch_id: идентификатор строения, которое привязывается к клиенту
            organization_id: идентификатор организации
        """
        pass

    @abstractmethod
    async def update_client_location(
            self,
            client_id: int,
            branch_id: int,
            organization_id: int
    ) -> Optional[storage_schem.clients_schem.LocationSchem]:
        """Абстрактный интерфейс метод для обновления
        местоположения клиента.
        Args:
            client_id: идентификатор клиента
            branch_id: идентификатор строения, которое привязывается к клиенту
            organization_id: идентификатор организации
        """
        pass
