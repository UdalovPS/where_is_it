from abc import ABC, abstractmethod
from typing import Optional

from schemas import storage_schem


class BaseBranchSchemas(ABC):
    """Интерфейс для работы с файлами"""
    @abstractmethod
    async def get_by_id(self, node_id: int) -> Optional[storage_schem.branches_schem.BranchSchema]:
        """Извлечение данных по первичному ключу
        Args:
            node_id: идентификатор записи
        """
        pass