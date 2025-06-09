from abc import ABC, abstractmethod
from typing import Optional

from schemas import storage_schem


class BaseBranchSchemas(ABC):
    """Интерфейс для работы с файлами"""
    @abstractmethod
    async def get_by_id(self, node_id: int) -> Optional[storage_schem.branches_schem.BranchPlanSchemaBase]:
        """Извлечение данных по первичному ключу
        Args:
            node_id: идентификатор записи
        """
        pass

    @abstractmethod
    async def get_data_by_branch_id(self, branch_id: int) -> Optional[storage_schem.branches_schem.BranchPlanSchemaBase]:
        """Извлечение данных по ID филиала
        Args:
            branch_id: идентификатор филиала
        """
        pass