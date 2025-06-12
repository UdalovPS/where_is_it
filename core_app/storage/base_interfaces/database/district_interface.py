from abc import ABC, abstractmethod
from typing import Optional, List

from schemas import storage_schem


class BaseDistrict(ABC):
    """Интерфейс класс хранящий данные о регионе"""
    @abstractmethod
    async def get_similar_by_org_country_and_name(
            self,
            organization_id: int,
            search_name: str,
            country_id: int,
            limit: int = 3,
            similarity_threshold: float = 0.1
    ) -> Optional[List[storage_schem.districts_schem.DistrictSchem]]:
        """Поиск списка похожих названий региона
        определенной организации
        Args:
            organization_id: идентификатор организации
            search_name: имя похожее на которое нужно найти
            country_id: идентификатор страны
            limit: кол-во извлекаемых записей
            similarity_threshold: доля похожести после которой запись входит в поле зрения
        """
        pass
