"""storage/database/db/postgres_alchemy/models/clients
Данные по странам
"""
from typing import Optional

from sqlalchemy import text, ForeignKey, select, update, JSON, Column, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
import logging

from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


class ClientsTable(Base):
    __tablename__ = "clients_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    frontend_service_id: Mapped[int] = mapped_column(ForeignKey("frontend_services_table.id", ondelete='CASCADE'))
    frontend_id = Column(BigInteger)
    frontend_data = Column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)

class ClientsDAL(database.BaseClient):
    async def get_data_by_frontend_id(
            self,
            frontend_id: int,
            frontend_service_id: int
    ) -> Optional[storage_schem.clients_schem.ClientWithLocationSchem]:
        """Извлечение данных клиента по типу мессенджера и ID из данного мессенджера
        Args:
            frontend_id: идентификатор клиента во внешнем фронтенд сервисе
            frontend_service_id: идентификатор фронтенд сервиса
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    # Execute raw SQL query
                    query = text("""
                            SELECT 
                                c.id AS client_id,
                                c.name AS client_name,
                                c.frontend_service_id,
                                c.frontend_id,
                                c.frontend_data,
                                c.created_at AS client_created_at,
                                c.update_at AS client_updated_at,
                                cl.id AS location_id,
                                cl.branch_id,
                                cl.created_at AS location_created_at,
                                cl.update_at AS location_updated_at
                            FROM 
                                clients_table c
                            LEFT JOIN 
                                client_location_table cl ON c.id = cl.client_id
                            WHERE 
                                c.frontend_id = :frontend_id 
                                AND c.frontend_service_id = :frontend_service_id
                        """)

                    result = await session.execute(
                        query,
                        {"frontend_id": frontend_id, "frontend_service_id": frontend_service_id}
                    )
                    row = result.fetchone()

                    if not row:
                        return None

                    # Convert row to dictionary
                    row_dict = dict(row._mapping)

                    # Build location data if exists
                    location = None
                    if row_dict.get("location_id"):
                        location = storage_schem.clients_schem.ClientLocationSchem(
                            id=row_dict["location_id"],
                            branch_id=row_dict["branch_id"],
                            created_at=row_dict["location_created_at"],
                            update_at=row_dict["location_updated_at"]
                        )

                    # Build client data
                    client = storage_schem.clients_schem.ClientWithLocationSchem(
                        id=row_dict["client_id"],
                        name=row_dict["client_name"],
                        frontend_service_id=row_dict["frontend_service_id"],
                        frontend_id=row_dict["frontend_id"],
                        frontend_data=row_dict["frontend_data"],
                        created_at=row_dict["client_created_at"],
                        update_at=row_dict["client_updated_at"],
                        location=location
                    )

                    return client

        except Exception as ex:
            logger.warning(f"Ошибка при извлечении данных клиента вместе с локацией: {frontend_id}, {frontend_service_id} -> {ex}")
            return None