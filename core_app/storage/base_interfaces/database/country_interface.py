from abc import ABC, abstractmethod
from typing import Optional, List

from schemas import storage_schem

class BaseCountry(ABC):
    """Интерфейс класс хранящий данные о стране"""
    @abstractmethod
    async def get_countries_by_org(self, organization_id: int) -> Optional[List[storage_schem.countries_schem.CountrySchem]]:
        """Извлекаем список стран одной организации
        Args:
              organization_id: идентификатор организации
        """
        pass
