from abc import ABC, abstractmethod
from typing import Optional

from schemas import storage_schem


class BaseClient(ABC):
    """Интерфейс класс хранящий данные о клиенте"""

    @abstractmethod
    async def get_data_by_frontend_id(
            self,
            frontend_id: int,
            frontend_service_id: int
    ) -> Optional[storage_schem.clients_schem.ClientWithLocationSchem]:
        """Извлечение данных клиента по типу мессенджера и ID из данного мессенджера
        Args:
            frontend_id: идентификатор клиента во внешнем фронтенд сервисе
            frontend_service_id: идентификатор фронтенд сервиса
        """
        pass
