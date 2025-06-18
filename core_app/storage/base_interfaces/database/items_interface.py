from abc import ABC, abstractmethod
from typing import Optional, List

from schemas import storage_schem


class BaseItems(ABC):
    """Интерфейс класс хранящий данные о товарах"""

    @abstractmethod
    async def get_similar_items(
            self, branch_id: int,
            search_name: str,
            organization_id: int,
            sim_threshold: float = 0.1,
            count: int = 10
    ) -> Optional[List[storage_schem.items_schem.SimilarItemsSchem]]:
        """Извлечение всех похожих по имени товаров лежащих
        на полках в помещении нужного филиала
        Args:
            branch_id: идентификатор филиала
            search_name: наименование по которому ведется поиск товара
            organization_id: идентификатор организации
            sim_threshold: процент похожести, по которому выдается поиск из БД
            count: кол-во записей которое нужно извлечь из БД
        """
