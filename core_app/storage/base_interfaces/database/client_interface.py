from abc import ABC, abstractmethod
from typing import Optional, Dict

from schemas import storage_schem


class BaseClient(ABC):
    """Интерфейс класс хранящий данные о клиенте"""

    @abstractmethod
    async def get_data_by_frontend_id(
            self,
            frontend_id: int,
            frontend_service_id: int,
            organization_id: int
    ) -> Optional[storage_schem.clients_schem.ClientWithLocationSchem]:
        """Извлечение данных клиента по типу мессенджера и ID из данного мессенджера
        Args:
            frontend_id: идентификатор клиента во внешнем фронтенд сервисе
            frontend_service_id: идентификатор фронтенд сервиса
            organization_id: идентификатор организации
        """
        pass

    @abstractmethod
    async def add_new_client(
            self,
            name: str,
            frontend_service_id: int,
            frontend_id: int,
            frontend_data: Optional[Dict]
    ) -> Optional[storage_schem.clients_schem.ClientWithLocationSchem]:
        """Добавление в БД данных нового клиента
        Args:
            name: имя клиента
            frontend_service_id: идентификатор фронтенд сервиса (1 - telegram)
            frontend_id: идентификатор клиента во фронтенд сервисе
            frontend_data: дополнительные данные о клиенте
        """
        pass
