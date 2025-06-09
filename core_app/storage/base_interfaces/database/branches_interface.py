from abc import ABC, abstractmethod


class BaseBranches(ABC):
    """Интерфейс класс хранящий данные о строении"""
    @abstractmethod
    async def get_data_by_id(self, node_id: int):
        """Извлечение данных помещения филиала по его ID
        Args:
            node_id: идентификатор филиала
        """
        pass
