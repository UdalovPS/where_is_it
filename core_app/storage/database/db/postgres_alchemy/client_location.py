"""storage/database/db/postgres_alchemy/models/client_location
Данные по странам
"""
from typing import Union, Any, Optional

from sqlalchemy import text, ForeignKey, select, update, JSON, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
import logging

from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


class ClientLocationTable(Base):
    __tablename__ = "client_location_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients_table.id", ondelete="CASCADE"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches_table.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)

class ClientLocationDAL(database.BaseClientLocation):
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
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    new_location = ClientLocationTable(
                        client_id=client_id,
                        branch_id=branch_id,
                        organization_id=organization_id
                    )
                    session.add(new_location)
                    await session.flush()
                    return storage_schem.clients_schem.LocationSchem.model_validate(new_location, from_attributes=True)
        except Exception as _ex:
            logger.critical(f"Ошибка при добавлении новой локации клиента: {client_id}, branch_id: {branch_id} -> {_ex}")

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
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = update(ClientLocationTable).where(
                        (ClientLocationTable.client_id == client_id) &
                        (ClientLocationTable.organization_id == organization_id)
                    ).values(branch_id=branch_id).returning(
                        ClientLocationTable.id,
                        ClientLocationTable.client_id,
                        ClientLocationTable.branch_id,
                        ClientLocationTable.organization_id
                    )
                    res = await session.execute(query)
                    await session.commit()
                    updated_data = res.mappings().first()
                    return storage_schem.clients_schem.LocationSchem.model_validate(updated_data)
        except Exception as ex:
            logger.critical(f"Ошибка при обновлении данных локации -> {ex}")