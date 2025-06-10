"""storage/database/just_db/branches"""
from typing import Optional, List

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class BranchesJustDb(database.BaseBranches):
    db = db_choicer.choice_branches_obj(db_type=config.DB_TYPE)

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
        return await self.db.get_data_by_geo(
            organization_id=organization_id,
            latitude=latitude,
            longitude=longitude,
            limit=limit
        )