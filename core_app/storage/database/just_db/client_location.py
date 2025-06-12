"""storage/database/just_db/branches"""
from typing import Optional, List, Any

from watchfiles import awatch

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class ClientLocationJustDb(database.BaseClientLocation):
    db = db_choicer.choice_client_location_obj(db_type=config.DB_TYPE)

    async def add_client_location(
            self,
            client_id: int,
            branch_id: Optional[int],
            organization_id: int
    ) -> Optional[storage_schem.clients_schem.LocationSchem]:
        """Абстрактный интерфейс метод для добавления
        назначения клиенту местонахождения.
        Args:
            client_id: идентификатор клиента
            branch_id: идентификатор строения, которое привязывается к клиенту
            organization_id: идентификатор организации
        """
        return await self.db.add_client_location(
            client_id=client_id,
            branch_id=branch_id,
            organization_id=organization_id
        )

    async def update_client_location(
            self,
            client_id: int,
            branch_id: int,
            organization_id: int
    ) -> Optional[storage_schem.clients_schem.LocationSchem]:
        """Абстрактный интерфейс метод для обновления
        местоположения клиента.
        Args:
            client_id: идентификатор клиента
            branch_id: идентификатор строения, которое привязывается к клиенту
            organization_id: идентификатор организации
        """
        return await self.db.update_client_location(
            client_id=client_id,
            branch_id=branch_id,
            organization_id=organization_id
        )