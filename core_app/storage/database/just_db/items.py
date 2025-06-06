"""storage/database/just_db/items"""
from typing import Optional, List

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class ItemsJustDb(database.BaseItems):
    db = db_choicer.choice_items_obj(db_type=config.DB_TYPE)

    async def get_similar_items(
            self, branch_id: int,
            search_name: str,
            sim_threshold: float = 0.1,
            count: int = 10
    ) -> Optional[List[storage_schem.items.SimilarItemsSchem]]:
        """Извлечение всех похожих по имени товаров лежащих
        на полках в помещении нужного филиала
        Args:
            branch_id: идентификатор филиала
            search_name: наименование по которому ведется поиск товара
            sim_threshold: процент похожести, по которому выдается поиск из БД
            count: кол-во записей которое нужно извлечь из БД
        """
        return await self.db.get_similar_items(
            branch_id=branch_id,
            search_name=search_name,
            sim_threshold=sim_threshold,
            count=count
        )