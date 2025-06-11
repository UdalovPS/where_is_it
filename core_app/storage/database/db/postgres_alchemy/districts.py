"""storage/database/db/postgres_alchemy/models/districts
Данные по странам
"""
from typing import Optional, List

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import logging

from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


class DistrictsTable(Base):
    __tablename__ = "districts_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries_table.id", ondelete="CASCADE"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class DistrictsDAL(database.BaseDistrict):
    async def get_similar_by_org_country_and_name(
            self,
            organization_id: int,
            search_name: str,
            country_id: int,
            limit: int = 3,
            similarity_threshold: float = 0.1
    ) -> Optional[List[storage_schem.districts_schem.DistrictSchem]]:
        """Поиск списка похожих названий региона
        определенной организации
        Args:
            organization_id: идентификатор организации
            search_name: имя похожее на которое нужно найти
            country_id: идентификатор страны
            limit: кол-во извлекаемых записей
            similarity_threshold: доля похожести после которой запись входит в поле зрения
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = text("""
                        SELECT
                            di.id AS district_id,
                            di.name AS district_name,
                            di.organization_id,
                            similarity(di.name, :search_name) AS similarity_score,
                            co.id AS country_id,
                            co.name AS country_name
                        FROM 
                            districts_table di
                        JOIN 
                            countries_table co ON co.id = di.country_id
                        WHERE 
                            di.organization_id = :organization_id
                            AND di.country_id = :country_id
                            AND similarity(di.name, :search_name) > :similarity_threshold
                        ORDER BY 
                            similarity_score DESC
                        LIMIT 
                            :limit
                    """)

                    result = await session.execute(
                        query,
                        {
                            "organization_id": organization_id,
                            "search_name": search_name,
                            "similarity_threshold": similarity_threshold,
                            "limit": limit,
                            "country_id": country_id
                        }
                    )
                    rows = result.fetchall()

                    if not rows:
                        return None
                    return [
                        storage_schem.districts_schem.DistrictSchem(
                            id=row.district_id,
                            name=row.district_name,
                            organization_id=row.organization_id,
                            country_data=storage_schem.countries_schem.CountrySchem(
                                id=row.country_id,
                                name=row.country_name,
                                organization_id=row.organization_id
                            )
                        ) for row in rows
                    ]

        except Exception as ex:
            logger.critical(
                f"Ошибка при извлечении похожих стран. {organization_id}, {search_name} -> {ex}")
            return None