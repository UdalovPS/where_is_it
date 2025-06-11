"""storage/database/db/postgres_alchemy/models/countries
Данные по странам
"""
from typing import Optional, List

from sqlalchemy import text, ForeignKey, select, update
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import logging

from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


class CountriesTable(Base):
    __tablename__ = "countries_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class CountriesDAL(database.BaseCountry):
    async def get_countries_by_org(self, organization_id: int) -> Optional[List[storage_schem.countries_schem.CountrySchem]]:
        """Извлекаем список стран одной организации
        Args:
              organization_id: идентификатор организации
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = text("""
                        SELECT
                            id,
                            name,
                            organization_id
                        FROM 
                            countries_table
                        WHERE 
                            organization_id = :organization_id 
                    """)

                    result = await session.execute(
                        query,
                        {"organization_id": organization_id}
                    )
                    rows = result.fetchall()

                    if not rows:
                        return None

                    return [
                        storage_schem.countries_schem.CountrySchem(
                            id=row.id,
                            name=row.id,
                            organization_id=row.organization_id
                        ) for row in rows
                    ]


        except Exception as ex:
            logger.warning(
                f"Ошибка при извлечении стран одной организации: {organization_id} -> {ex}")
            return None