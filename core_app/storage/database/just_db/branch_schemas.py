"""storage/database/just_db/branch_schemas"""
from typing import Optional

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class BranchSchemasJustDb(database.BaseBranchSchemas):
    """Данный объект отвечает за взаимодействие с БД
    касающимися схем филиалов (работы с файлами)
    """
    db = db_choicer.choice_branch_schemas_obj(db_type=config.DB_TYPE)

    async def get_by_id(self, node_id: int) -> Optional[storage_schem.branches_schem.BranchSchema]:
        """Извлечение данных по первичному ключу
        Args:
            node_id: идентификатор записи
        """
        return await self.db.get_by_id(node_id=node_id)