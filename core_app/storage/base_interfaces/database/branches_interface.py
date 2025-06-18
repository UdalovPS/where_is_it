from abc import ABC, abstractmethod
from typing import  Optional, List

from schemas import storage_schem


class BaseBranches(ABC):
    """Интерфейс класс хранящий данные о строении"""
    @abstractmethod
    async def get_data_by_geo(
            self,
            organization_id: int,
            latitude: float,
            longitude: float,
            limit: int
    ) -> Optional[List[storage_schem.branches_schem.BranchSchema]]:
        """Извлечение ближайших к текущей геолокации филиалов
        Args:
            organization_id: идентификатор организации
            latitude: широта, от которой требуется вести поиск
            longitude: долгота от который требуется вести поиск
            limit: кол-во записей, которые нужно вернуть
        """
        pass

    @abstractmethod
    async def get_similar_by_org_city_and_address(
            self,
            organization_id: int,
            city_id: int,
            search_address: str,
            limit: int = 3,
            similarity_threshold: float = 0.1
    ) -> Optional[List[storage_schem.branches_schem.BranchSchema]]:
        """Поиск списка похожих названий населенного пункта
        определенной организации
        Args:
            organization_id: идентификатор организации
            city_id: идентификатор города в котором нужно найти филиал
            search_address: адрес поиска
            limit: кол-во извлекаемых записей
            similarity_threshold: доля похожести после которой запись входит в поле зрения
        """
        pass

    @abstractmethod
    async def get_branch_data_by_id(self, node_id: int) -> Optional[storage_schem.branches_schem.BranchSchema]:
        """Извлекаем данные филиала по его ID
        Args:
            node_id: идентификатор записи
        """
        pass
