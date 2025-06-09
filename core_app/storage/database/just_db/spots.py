"""storage/database/just_db/spots"""
from typing import Optional, List

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class SpotsJustDb(database.BaseSpot):
    db = db_choicer.choice_spots_obj(db_type=config.DB_TYPE)

    async def get_data_by_item_and_organization(
            self,
            items_ids: List[int],
            org_id: int,
            branch_id: int
    ) -> Optional[List[storage_schem.spots_schem.SpotsWithShelvesSchem]]:
        """Извлечение данных по товару и организации
        Args:
            items_ids: список идентификаторов товаров которые необходим найти на полках
            org_id: идентификатор организации
            branch_id: идентификатор филиала в котором осуществляется поиск
        """
        return await self.db.get_data_by_item_and_organization(items_ids=items_ids, org_id=org_id, branch_id=branch_id)