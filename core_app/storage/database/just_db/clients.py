"""storage/database/just_db/clients"""
from typing import Optional

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class ClientsJustDb(database.BaseClient):
    """Данный объект отвечает за взаимодействие с БД
    касающимися для получения данных клиента
    """
    db = db_choicer.choice_db_client_obj(db_type=config.DB_TYPE)

    async def get_data_by_frontend_id(
            self,
            frontend_id: int,
            frontend_service_id: int
    ) -> Optional[storage_schem.clients_schem.ClientWithLocationSchem]:
        return await self.db.get_data_by_frontend_id(
            frontend_id=frontend_id, frontend_service_id=frontend_service_id
        )
