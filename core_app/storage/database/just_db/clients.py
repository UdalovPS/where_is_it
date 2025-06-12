"""storage/database/just_db/clients"""
from typing import Optional, Dict

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
            frontend_service_id: int,
            organization_id: int
    ) -> Optional[storage_schem.clients_schem.ClientWithLocationSchem]:
        return await self.db.get_data_by_frontend_id(
            frontend_id=frontend_id,
            frontend_service_id=frontend_service_id,
            organization_id=organization_id
        )

    async def add_new_client(
            self,
            name: str,
            frontend_service_id: int,
            frontend_id: int,
            frontend_data: Optional[Dict] = None
    ) -> Optional[storage_schem.clients_schem.ClientWithLocationSchem]:
        """Добавление в БД данных нового клиента
        Args:
            name: имя клиента
            frontend_service_id: идентификатор фронтенд сервиса (1 - telegram)
            frontend_id: идентификатор клиента во фронтенд сервисе
            frontend_data: дополнительные данные о клиенте
        """
        return await self.db.add_new_client(
            name=name,
            frontend_service_id=frontend_service_id,
            frontend_id=frontend_id,
            frontend_data=frontend_data
        )