"""storage/database/db/postgres_alchemy/models/sities
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


class CitiesTable(Base):
    __tablename__ = "cities_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts_table.id", ondelete="CASCADE"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class CitiesDAL(database.BaseCity):
    async def get_similar_by_org_district_and_name(
            self,
            organization_id: int,
            search_name: str,
            district_id: int,
            limit: int = 3,
            similarity_threshold: float = 0.1
    ) -> Optional[List[storage_schem.cities_schem.CitySchem]]:
        """Поиск списка похожих названий населенного пункта
        определенной организации
        Args:
            organization_id: идентификатор организации
            search_name: имя похожее на которое нужно найти
            district_id: идентификатор региона
            limit: кол-во извлекаемых записей
            similarity_threshold: доля похожести после которой запись входит в поле зрения
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = text("""
                        SELECT
                            ci.id AS city_id,
                            ci.name AS city_name,
                            ci.organization_id,
                            di.id AS district_id,
                            di.name AS district_name,
                            similarity(ci.name, :search_name) AS similarity_score,
                            co.id AS country_id,
                            co.name AS country_name
                        FROM 
                            cities_table ci
                        JOIN 
                            districts_table di ON di.id = ci.district_id
                        JOIN 
                            countries_table co ON co.id = di.country_id
                        WHERE 
                            di.organization_id = :organization_id
                            AND ci.district_id = :district_id
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
                            "district_id": district_id
                        }
                    )
                    rows = result.fetchall()

                    if not rows:
                        return None
                    return [
                        storage_schem.cities_schem.CitySchem(
                            id=row.city_id,
                            name=row.city_name,
                            organization_id=row.organization_id,
                            district_data=storage_schem.districts_schem.DistrictSchem(
                                id=row.district_id,
                                name=row.district_name,
                                organization_id=row.organization_id,
                                country_data=storage_schem.countries_schem.CountrySchem(
                                    id=row.country_id,
                                    name=row.country_name,
                                    organization_id=row.organization_id
                                )
                            )
                        ) for row in rows
                    ]

        except Exception as ex:
            logger.critical(
                f"Ошибка при извлечении похожих городов. {organization_id}, {search_name} -> {ex}")
            return None
